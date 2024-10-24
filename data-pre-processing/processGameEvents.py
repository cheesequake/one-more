import json

def process_game_events(file_path):
    """
    process_game_events

    :param file_path: A game JSON file which contains game events
    :return: a JSON array of each individual player stats
    """

    with open(file_path, 'r') as file:
        events = json.load(file)

    player_stats = {i: {
        'attackKills': 0, 'defenseKills': 0, 'attackDeaths': 0, 'defenseDeaths': 0,
        'attackAssists': 0, 'defenseAssists': 0, 'attackFirstKills': 0, 'attackFirstDeaths': 0,
        'defenseFirstKills': 0, 'defenseFirstDeaths': 0, 'aces': 0, 'fourKills': 0,
        'headShots': 0, 'totalShots': 0, 'operatorKills': 0, 'ACS': 0, 'pistolKills': 0, 'selectedAgent': "",
        'selectedAgentKDA': 0
    } for i in range(1, 11)}

    agent_mapping = {
        "add6443a-41bd-e414-f6ad-e58d267f4e95": "Jett",
        "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc": "Reyna",
        "f94c3b30-42be-e959-889c-5aa313dba261": "Raze",
        "7f94d92c-4234-0a36-9646-3a87eb8b5c89": "Yoru",
        "eb93336a-449b-9c1b-0a54-a891f7921d69": "Phoenix",
        "bb2a4828-46eb-8cd1-e765-15848195d751": "Neon",
        "5f8d3a7f-467b-97f3-062c-13acf203c006": "Breach",
        "6f2a04ca-43e0-be17-7f36-b3908627744d": "Skye",
        "320b2a48-4d9b-a075-30f1-1f93a9b638fa": "Sova",
        "601dbbe7-43ce-be57-2a40-4abd24953621": "Kayo",
        "1e58de9c-4950-5125-93e9-a0aee9f98746": "Killjoy",
        "117ed9e3-49f3-6512-3ccf-0cada7e3823b": "Cypher",
        "569fdd95-4d10-43ab-ca70-79becc718b46": "Sage",
        "22697a3d-45bf-8dd7-4fec-84a9e28c69d7": "Chamber",
        "8e253930-4c05-31dd-1b6c-968525494517": "Omen",
        "9f0d8ba9-4140-b941-57d3-a7ad57c6b417": "Brimstone",
        "41fb69c1-4189-7b37-f117-bcaf1e96f1bf": "Astra",
        "707eab51-4836-f488-046a-cda6bf494859": "Viper",
        "dade69b4-4f5a-8528-247b-219e5a1facd6": "Fade",
        "95b78ed7-4637-86d9-7e41-71ba8c293152": "Harbor",
        "e370fa57-4757-3604-3648-499e1f642d3f": "Gekko",
        "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235": "Deadlock",
        "0e38b510-41a8-5780-5e8f-568b2a4f2d6c": "Iso",
        "1dbf2edd-4729-0984-3115-daa5eed44993": "Clove",
        "efba5359-4016-a1e5-7626-b1ae76895940": "Vyse"
    }

    # Variable to track if all players have selectedAgent populated
    all_agents_assigned = False

    # Function to update KDA for attack or defense side
    def update_stats(player_id, kills, deaths, assists, is_attacking):
        if is_attacking:
            player_stats[player_id]['attackKills'] += kills
            player_stats[player_id]['attackDeaths'] += deaths
            player_stats[player_id]['attackAssists'] += assists
        else:
            player_stats[player_id]['defenseKills'] += kills
            player_stats[player_id]['defenseDeaths'] += deaths
            player_stats[player_id]['defenseAssists'] += assists

    # Helper function to determine if player is attacking or defending based on round
    def is_attacking(player_id, round):
        if round <= 11:
            return player_id >= 6  # Players 6-10 attack in rounds 0-11
        elif round <= 23:
            return player_id <= 5  # Players 1-5 attack in rounds 12-23
        else:
            # Sudden death rounds (starting from round 24)
            return (round % 2 == 0) if player_id >= 6 else (round % 2 != 0)

    for event in events:
        # Process the configuration event to populate selectedAgent for each player
        if 'configuration' in event and 'players' in event['configuration'] and not all_agents_assigned:
            for player in event['configuration']['players']:
                player_id = int(player['playerId']['value'])
                agent_guid = player['selectedAgent']['fallback']['guid'].lower()

                # Map the agent GUID to the agent name and assign it to the player's selectedAgent
                agent_name = agent_mapping.get(agent_guid, "Unknown Agent")
                if player_id in player_stats:
                    player_stats[player_id]['selectedAgent'] = agent_name

            all_agents_assigned = all(player_stats[player_id]['selectedAgent'] != "" for player_id in player_stats)
            continue

    total_rounds = 0
    # Loop through all events and calculate the total rounds
    for event in events:
        # Update total_rounds from the gamePhase roundNumber, which is 0-indexed
        if 'gamePhase' in event and 'roundNumber' in event['gamePhase']:
            current_round = event['gamePhase'].get('roundNumber', 0) + 1  # Since roundNumber is 0-indexed
            total_rounds = max(total_rounds, current_round)

        # Check for gameDecided event to get the totalRounds and stop processing further events
        if 'gameDecided' in event and 'spikeMode' in event['gameDecided']:
            completed_rounds = event['gameDecided']['spikeMode'].get('completedRounds', [])
            if completed_rounds:
                total_rounds = max(total_rounds, max(round['roundNumber'] for round in completed_rounds))
            break

    # If total_rounds is still 0, skip processing this file
    if total_rounds == 0:
        print(f"Skipping file {file_path} due to no valid round data.")
        return

    # Dictionary to store the last snapshot per round
    last_snapshots = {}

    # Set to track rounds we've already processed
    visited_rounds = set()

    # Variable to track the current round number
    current_round = None

    # Variable to store the last snapshot for the current round
    current_snapshot = None

    # Traverse the events to find the last snapshot for each round
    for event in events:
        # Check if the event is related to gamePhase
        if 'gamePhase' in event and 'phase' in event['gamePhase']:
            phase = event['gamePhase']['phase']
            round_number = event['gamePhase'].get('roundNumber', None)

            # If phase is ROUND_STARTING, store the last snapshot for the previous round
            if phase == 'ROUND_STARTING' and round_number is not None:
                if current_round is not None and current_snapshot is not None:
                    # Store the last snapshot of the previous round
                    last_snapshots[current_round] = current_snapshot

                # Update current round number and reset snapshot tracking for the new round
                current_round = round_number
                current_snapshot = None  # Reset for the new round

        # Handle snapshot events separately
        if 'snapshot' in event and 'players' in event['snapshot']:
            # If there's a current round, update the snapshot for that round
            if current_round is not None:
                current_snapshot = event['snapshot']  # Capture the snapshot during the current round

    # After the loop, store the final snapshot if the last round had one
    if current_round is not None and current_snapshot is not None:
        last_snapshots[current_round] = current_snapshot

    # Process all rounds
    last_snapshot = None
    for round in range(total_rounds):
        snapshot = last_snapshots.get(round)

        if snapshot and round not in visited_rounds:
            for player in snapshot['players']:
                player_id = int(player['playerId']['value'])
                kills = player['kills']
                deaths = player['deaths']
                assists = player['assists']
                is_player_attacking = is_attacking(player_id, round)
                if round == total_rounds - 1:
                    total_score = player.get('scores', {}).get('combatScore', {}).get('totalScore', 0)
                    average_score = total_score / total_rounds
                    player_stats[player_id]['ACS'] = average_score

                if last_snapshot:
                    # Subtract the previous snapshot KDA to get KDA for this round and after
                    prev_player = next((p for p in last_snapshot['players'] if int(p['playerId']['value']) == player_id), None)
                    if prev_player:
                        round_kills = kills - prev_player['kills']
                        round_deaths = deaths - prev_player['deaths']
                        round_assists = assists - prev_player['assists']
                        update_stats(player_id, round_kills, round_deaths, round_assists, is_player_attacking)
                else:
                    # First snapshot, just add all KDA directly
                    update_stats(player_id, kills, deaths, assists, is_player_attacking)

            # Mark this round as visited
            visited_rounds.add(round)
            last_snapshot = snapshot

    round_kill_tracker = {}  # Track kills for each player per round
    first_kill_tracked_rounds = set()  # Track rounds where first kill/death was counted

    # Variable to track the current round
    current_round = None

    # Traverse the events
    for event in events:
        # Check for gamePhase events to track rounds
        if 'gamePhase' in event and 'phase' in event['gamePhase']:
            phase = event['gamePhase']['phase']
            round_number = event['gamePhase'].get('roundNumber', None)

            # Mark the start of a round
            if phase == 'ROUND_STARTING' and round_number is not None:
                current_round = round_number  # Update the current round
                # Reset kill tracking for the new round
                if current_round not in round_kill_tracker:
                    round_kill_tracker[current_round] = {}

        # Process damageEvent
        if 'damageEvent' in event:
            causer = event['damageEvent'].get('causerId')
            victim = event['damageEvent'].get('victimId')

            # Ensure causerId and victimId are valid before processing
            if causer and 'value' in causer and victim and 'value' in victim:
                causer_id = int(causer['value'])
                victim_id = int(victim['value'])

                # Process shot-related events
                if 'location' in event['damageEvent']:
                    location = event['damageEvent']['location']
                    # Only count totalShots for valid locations (HEAD, BODY, LEG)
                    if location in ["HEAD", "BODY", "LEG"]:
                        player_stats[causer_id]['totalShots'] += 1
                        if location == "HEAD":
                            player_stats[causer_id]['headShots'] += 1

                # Process kill events
                if 'killEvent' in event['damageEvent'] and event['damageEvent']['killEvent'] == True:
                    # Track operator kills
                    if 'weapon' in event['damageEvent'] and 'fallback' in event['damageEvent']['weapon'] and \
                    event['damageEvent']['weapon']['fallback']['guid'] == "A03B24D3-4319-996D-0F8C-94BBFBA1DFC7":
                        player_stats[causer_id]['operatorKills'] += 1

                    # Track pistol kills
                    pistol_guids = [
                        "E336C6B8-418D-9340-D77F-7A9E4CFE0702",
                        "29A0CFAB-485B-F5D5-779A-B59F85E204A8",
                        "1BAA85B4-4C70-1284-64BB-6481DFC3BB4E",
                        "44D4E95C-4157-0037-81B2-17841BF2E8E3",
                        "42DA8CCC-40D5-AFFC-BEEC-15AA47B42EDA"
                    ]
                    if 'weapon' in event['damageEvent'] and 'fallback' in event['damageEvent']['weapon'] and \
                    event['damageEvent']['weapon']['fallback']['guid'] in pistol_guids:
                        player_stats[causer_id]['pistolKills'] += 1

                    # Determine if causer and victim were attacking or defending
                    is_causer_attacking = is_attacking(causer_id, current_round)
                    is_victim_attacking = is_attacking(victim_id, current_round)

                    # Track first kill and death for the round if not already done
                    if current_round not in first_kill_tracked_rounds:
                        if is_causer_attacking:
                            player_stats[causer_id]['attackFirstKills'] += 1
                        else:
                            player_stats[causer_id]['defenseFirstKills'] += 1

                        if is_victim_attacking:
                            player_stats[victim_id]['attackFirstDeaths'] += 1
                        else:
                            player_stats[victim_id]['defenseFirstDeaths'] += 1

                        first_kill_tracked_rounds.add(current_round)

                    # Track kills for aces and four kills
                    if causer_id not in round_kill_tracker[current_round]:
                        round_kill_tracker[current_round][causer_id] = 0
                    round_kill_tracker[current_round][causer_id] += 1

                    # Check for four kills or aces
                    if round_kill_tracker[current_round][causer_id] == 4:
                        player_stats[causer_id]['fourKills'] += 1
                    elif round_kill_tracker[current_round][causer_id] >= 5:
                        player_stats[causer_id]['aces'] += 1

    for player_id in range(1, 11):
        attack_kills = player_stats[player_id]['attackKills']
        defense_kills = player_stats[player_id]['defenseKills']
        attack_deaths = player_stats[player_id]['attackDeaths']
        defense_deaths = player_stats[player_id]['defenseDeaths']

        # Calculate total kills, assists, and deaths
        total_kills = attack_kills + defense_kills + player_stats[player_id]['attackAssists'] + player_stats[player_id]['defenseAssists']
        total_deaths = attack_deaths + defense_deaths

        # Calculate KDA
        if total_deaths > 0:
            player_stats[player_id]['selectedAgentKDA'] = (total_kills) / total_deaths
        else:
            player_stats[player_id]['selectedAgentKDA'] = total_kills

    return player_stats

# print (json.dumps(process_game_events ("./vct-international/games/2023/val_767b9ffd-c228-4b74-9723-08552caa063f.json"), indent=4))