const fs = require('fs');

// Create a team league mapping from the teams file
function createTeamLeagueMapping(inputFilePath, outputFilePath) {
  fs.readFile(inputFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading the input file:', err);
      return;
    }

    try {
      const teams = JSON.parse(data);

      const teamLeagueMapping = teams.map(team => ({
        team_id: team.id,
        home_league_id: team.home_league_id
      }));

      fs.writeFile(outputFilePath, JSON.stringify(teamLeagueMapping, null, 2), (err) => {
        if (err) {
          console.error('Error writing to the output file:', err);
          return;
        }
        console.log('Team league mapping has been created successfully!');
      });

    } catch (err) {
      console.error('Error parsing the JSON data:', err);
    }
  });
}

// // Example usage
// const inputFilePath = './vct-international/esports-data/teams.json';
// const outputFilePath = './vct-international/esports-data/team_league_mapping.json';

// createTeamLeagueMapping(inputFilePath, outputFilePath);
