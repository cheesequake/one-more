## Data Pre-Processing

Documents all my data pre-processing steps

### Downloading Data

Use the file [downloadFromS3.js](./downloadFromS3.js) to download data from the public S3 bucket. NOTE: You might have to run the function multiple times, as the download may time out. But don't worry, it only downloads the remaining files.

### Extracting, Zipping and Deleting Files

Use the following files if you want to extract/zip files from a folder:
- [extractJSON.py](./extractJSON.py): extract all files in a folder.
- [zipJSON.py](./zipJSON.py): zip all JSON files in a folder.
- [deleteFilesOfType.py](./deleteFilesOfType.py): delete all files of the given type from a folder.

### Set up a Database

We need to store all the data in a database. Personally, I used a AWS RDS MySQL Free Tier version to minimise costs. The file [sqlExecutor.py](./sqlExecutor.py) contains functions to connect to, and execute queries on your database.

### Analyse Esports Data

Now that we have the game data all downloaded, we will analyse the esports folder first. The following files allow us to process and insert data.
- [processLeagues.py](./processLeagues.py): Extract league information from a JSON file
- [processTeams.py](./processTeams.py): Extract team information from a JSON file
- [createTeamLeagueMapping.js]: From the teams files, create a team-league mapping
- [removeDuplicates.js](./removeDuplicates.js): Remove duplicate team and league mappings
- [processTeamLeagueMapping.py](./processTeamLeagueMapping.py): Extract team league mapping information and send to database
- [agent_mapping.json](./agent_mapping.json): Agent data from the existing VALORANT agents
- [insertAgentData.py](./insertAgentData.py): Insert Agent data to SQL
- [initPlayerData.js](./initPlayerData.js): Initialise player data from players file into an overall data pool
- [processGameEvents.py](./processGameEvents.py): Process and extract player stats from a single game json file
- [processAllGames.py](./processAllGames.py): Process and extract player stats from all games in a folder utilising processGameEvents (above)
- [assignIGL.py](./assignIGL.py): Assign IGL to the player ID passed
- [insertPlayerData.py](./insertPlayerData.py): Insert player data into the database
- [util.py](./util.py): Miscellaneous helper functions