const fs = require('fs');

// Prettify JSON to look better
function prettifyJSONFile(filePath) {
    try {
        const jsonData = fs.readFileSync(filePath, 'utf-8');

        const jsonObject = JSON.parse(jsonData);
        const prettyJson = JSON.stringify(jsonObject, null, 2);

        const outputFilePath = filePath.replace('.json', '_pretty.json');
        fs.writeFileSync(outputFilePath, prettyJson, 'utf-8');

        console.log(`Prettified JSON saved to: ${outputFilePath}`);
    } catch (error) {
        console.error("Error processing JSON file:", error);
    }
}

// // Example usage: pass the file path as an argument
// const filePath = "./vct-international/games/2023/val_ff229eca-643c-4d87-a33e-b5de43fcc2d1.json";
// prettifyJSONFile(filePath);
