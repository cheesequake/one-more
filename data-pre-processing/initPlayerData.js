const fs = require('fs');

// Create a file from player data and initialise data
function processPlayerData(inputFilePath, outputFilePath, level) {
    const inputData = JSON.parse(fs.readFileSync(inputFilePath, 'utf8'));

    let outputData = [];
    if (fs.existsSync(outputFilePath)) {
        outputData = JSON.parse(fs.readFileSync(outputFilePath, 'utf8'));
    }

    inputData.forEach(player => {
        const { id, handle, first_name, last_name, status, home_team_id, created_at } = player;

        const existingPlayer = outputData.find(p => p.id === id && p.home_team_id === home_team_id);

        if (existingPlayer) {
            if (level !== existingPlayer.level) {
                existingPlayer.level = level;
            }
            // Check if the new player data has a more recent 'created_at'
            if (new Date(created_at) > new Date(existingPlayer.created_at)) {
                existingPlayer.inGameName = handle;
                existingPlayer.first_name = first_name;
                existingPlayer.last_name = last_name;
                existingPlayer.status = status;
                existingPlayer.created_at = created_at;
            }
        } else {
            // Create new player data with initialized stats
            outputData.push({
                id,
                inGameName: handle,
                first_name,
                last_name,
                status,
                home_team_id,
                created_at,
                attackKills2022: 0,
                attackKills2023: 0,
                attackKills2024: 0,
                defenseKills2022: 0,
                defenseKills2023: 0,
                defenseKills2024: 0,
                attackDeaths2022: 0,
                attackDeaths2023: 0,
                attackDeaths2024: 0,
                defenseDeaths2022: 0,
                defenseDeaths2023: 0,
                defenseDeaths2024: 0,
                attackAssists2022: 0,
                attackAssists2023: 0,
                attackAssists2024: 0,
                defenseAssists2022: 0,
                defenseAssists2023: 0,
                defenseAssists2024: 0,
                attackFirstKills: 0,
                attackFirstDeaths: 0,
                defenseFirstKills: 0,
                defenseFirstDeaths: 0,
                aces: 0,
                fourKills: 0,
                headShots: 0,
                totalShots: 0,
                operatorKills: 0,
                ACS: 0,
                pistolKills: 0,
                matchesPlayed: 0,
                level: level,
                matchesAsJett: 0,
                JettKDA: 0,
                matchesAsReyna: 0,
                ReynaKDA: 0,
                matchesAsRaze: 0,
                RazeKDA: 0,
                matchesAsYoru: 0,
                YoruKDA: 0,
                matchesAsPhoenix: 0,
                PhoenixKDA: 0,
                matchesAsNeon: 0,
                NeonKDA: 0,
                matchesAsBreach: 0,
                BreachKDA: 0,
                matchesAsSkye: 0,
                SkyeKDA: 0,
                matchesAsSova: 0,
                SovaKDA: 0,
                matchesAsKayo: 0,
                KayoKDA: 0,
                matchesAsKilljoy: 0,
                KilljoyKDA: 0,
                matchesAsCypher: 0,
                CypherKDA: 0,
                matchesAsSage: 0,
                SageKDA: 0,
                matchesAsChamber: 0,
                ChamberKDA: 0,
                matchesAsOmen: 0,
                OmenKDA: 0,
                matchesAsBrimstone: 0,
                BrimstoneKDA: 0,
                matchesAsAstra: 0,
                AstraKDA: 0,
                matchesAsViper: 0,
                ViperKDA: 0,
                matchesAsFade: 0,
                FadeKDA: 0,
                matchesAsHarbor: 0,
                HarborKDA: 0,
                matchesAsGekko: 0,
                GekkoKDA: 0,
                matchesAsDeadlock: 0,
                DeadlockKDA: 0,
                matchesAsIso: 0,
                IsoKDA: 0,
                matchesAsClove: 0,
                CloveKDA: 0,
                matchesAsVyse: 0,
                VyseKDA: 0,
            });
        }
    });

    // Sort the output data by the player's handle alphabetically
    outputData.sort((a, b) => a.inGameName.localeCompare(b.inGameName));

    // Write the sorted output to the output file
    fs.writeFileSync(outputFilePath, JSON.stringify(outputData, null, 2), 'utf8');
    console.log(`Player data saved and sorted by handle to ${outputFilePath}`);
}

// Example usage
// processPlayerData('./game-changers/esports-data/players.json', './allPlayersAllData.json', 'Game-Changer');
// processPlayerData('./vct-challengers/esports-data/players.json', './allPlayersAllData.json', 'Semi-Professional');
// processPlayerData('./vct-international/esports-data/players.json', './allPlayersAllData.json', 'Professional');
