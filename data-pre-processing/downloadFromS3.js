const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');
const util = require('util');
const sleep = util.promisify(setTimeout);

AWS.config.update({
  accessKeyId: '', // Replace with your Access Key
  secretAccessKey: '', // Replace with your Secret Key
  region: '', // Replace with your region
});

const s3 = new AWS.S3();

const bucketName = 'vcthackathon-data';
const localDir = '.'; // Where the data would be downloaded

async function getS3FileSize(key) {
  const params = {
    Bucket: bucketName,
    Key: key,
  };

  try {
    const headObject = await s3.headObject(params).promise();
    return headObject.ContentLength;
  } catch (err) {
    console.error(`Error fetching metadata for ${key}: ${err.message}`);
    return null;
  }
}

async function fileNeedsRedownload(filePath, s3Size) {
  try {
    const stats = fs.statSync(filePath);
    return stats.size < s3Size;
  } catch (err) {
    return true;
  }
}

async function downloadFile(key, retryCount = 3) {
  const sanitizedKey = key.replace(/[:]/g, '_');
  const filePath = path.join(localDir, sanitizedKey);

  const s3FileSize = await getS3FileSize(key);
  if (s3FileSize === null) {
    console.error(`Skipping ${key} due to metadata fetch error.`);
    return;
  }

  const needsRedownload = await fileNeedsRedownload(filePath, s3FileSize);

  if (!needsRedownload) {
    console.log(`Skipping ${key}, already downloaded and up-to-date.`);
    return;
  }

  fs.mkdirSync(path.dirname(filePath), { recursive: true });

  const params = {
    Bucket: bucketName,
    Key: key,
  };

  for (let attempt = 1; attempt <= retryCount; attempt++) {
    try {
      const fileStream = fs.createWriteStream(filePath);
      const s3Stream = s3.getObject(params).createReadStream();

      s3Stream.pipe(fileStream);

      s3Stream.on('error', async (err) => {
        console.error(`Error downloading ${key}: ${err.message}`);
        fileStream.close();
        throw err;
      });

      await new Promise((resolve, reject) => {
        fileStream.on('finish', () => {
          console.log(`Downloaded ${key} to ${filePath}`);
          resolve();
        });

        fileStream.on('error', (err) => {
          console.error(`Error writing file ${key}: ${err.message}`);
          reject(err);
        });
      });

      break;

    } catch (error) {
      console.error(`Attempt ${attempt} failed for ${key}: ${error.message}`);
      await sleep(2000);

      if (attempt === retryCount) {
        console.error(`Max retries reached for ${key}. Moving to next file.`);
      }
    }
  }
}

async function downloadAllFiles() {
  let continuationToken = null;

  do {
    const params = {
      Bucket: bucketName,
      ContinuationToken: continuationToken,
    };

    try {
      const data = await s3.listObjectsV2(params).promise();

      const downloadPromises = data.Contents.map((item) =>
        downloadFile(item.Key)
      );
      await Promise.all(downloadPromises);

      continuationToken = data.IsTruncated ? data.NextContinuationToken : null;
    } catch (err) {
      console.error('Error listing objects:', err);
      break;
    }
  } while (continuationToken);
}

downloadAllFiles().catch((err) => {
  console.error('Error downloading files:', err);
});
