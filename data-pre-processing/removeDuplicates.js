const fs = require('fs');

// Function to remove duplicate objects based on team_id and home_league_id
function removeDuplicates(data) {
    const uniqueItems = [];
    const seen = new Set();

    for (const item of data) {
        const identifier = `${item.team_id}-${item.home_league_id}`;
        if (!seen.has(identifier)) {
            seen.add(identifier);
            uniqueItems.push(item);
        }
    }

    return uniqueItems;
}

// Main function to process the JSON file
function processJsonFile(filePath) {
    try {
        const jsonData = fs.readFileSync(filePath, 'utf-8');
        const data = JSON.parse(jsonData);

        if (!Array.isArray(data)) {
            throw new Error('JSON data is not an array.');
        }

        const cleanedData = removeDuplicates(data);

        fs.writeFileSync(filePath, JSON.stringify(cleanedData, null, 2));

        console.log('Duplicates removed and file updated successfully.');
    } catch (err) {
        console.error('Error processing JSON file:', err);
    }
}

// // Example usage: Pass the path of the JSON file
// const jsonFilePath = '';  // Replace with your actual file path
// processJsonFile(jsonFilePath);
