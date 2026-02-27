# imports
import random
import time

# variables
rewardAmount = 0.1
rewardRange = 5.0
rewardAcceleration = 1.0
agentAcceleration = 2.0

explorationRate = 0.1
learningRate = 0.2
futureWeight = 0.2
gameBoundaries = 100.0
timeLimit = 100
episodeNum = 1000
map_width = 40

Q = {}

playtime = 0

for episode in range(episodeNum):
    # reset
    rewardPosition = 0.0
    rewardSpeed = 0.0
    agentPosition = 0.0
    agentSpeed = 0.0
    controlPressed = False
    score = 0.0
    explorationRate *= 0.95

    fps = 5 if episode == episodeNum - 1 else 0

    # initial
    distance = rewardPosition - agentPosition
    distanceCategory = "far_up" if distance > rewardRange else \
                       "near_up" if distance > 0 else \
                       "near_down" if distance >= -rewardRange else \
                       "far_down"
    agentSpeedCategory = "up" if agentSpeed > 0 else "down"
    rewardSpeedCategory = "up" if rewardSpeed > 0 else "down"
    state = (distanceCategory, agentSpeedCategory, rewardSpeedCategory)
    if state not in Q:
        Q[state] = {True: 0.0, False: 0.0}

    # main loop
    for t in range(timeLimit):
        # decide action
        if random.random() < explorationRate:
            controlPressed = random.choice([True, False])
        else:
            controlPressed = max(Q[state], key=Q[state].get)

        # physics
        agentSpeed += agentAcceleration if controlPressed else -agentAcceleration
        agentPosition += agentSpeed
        if abs(agentPosition) > gameBoundaries:
            agentPosition = 100 * (agentPosition / abs(agentPosition))

        rewardSpeed = rewardAcceleration * random.randint(-1, 1)
        rewardPosition += rewardSpeed
        if abs(rewardPosition) > gameBoundaries:
            rewardPosition = 100 * (rewardPosition / abs(rewardPosition))

        # categorize state
        distance = rewardPosition - agentPosition
        distanceCategory = "far_up" if distance > rewardRange else \
                           "near_up" if distance > 0 else \
                           "near_down" if distance >= -rewardRange else \
                           "far_down"
        agentSpeedCategory = "up" if agentSpeed > 0 else "down"
        rewardSpeedCategory = "up" if rewardSpeed > 0 else "down"
        stateNext = (distanceCategory, agentSpeedCategory, rewardSpeedCategory)
        if stateNext not in Q:
            Q[stateNext] = {True: 0.0, False: 0.0}

        # reward
        reward = -abs(distance) * 0.01
        if abs(distance) < rewardRange:
            reward += 1
        score += reward
        max_possible_score = t + 1  # time steps start at 0
        precision = (score / max_possible_score) * 100

        # Q learning update
        futureBest = max(Q[stateNext].values())
        Q[state][controlPressed] += learningRate * (reward + futureWeight * futureBest - Q[state][controlPressed])
        state = stateNext

        # visualizer
        if fps != 0:
            print("\033c\033[3J", end='')  # clear screen

            # map line
            line = ["-"] * map_width
            agent_idx = int((agentPosition + gameBoundaries) / (2 * gameBoundaries) * (map_width - 1))
            reward_idx = int((rewardPosition + gameBoundaries) / (2 * gameBoundaries) * (map_width - 1))
            if agent_idx == reward_idx:
                line[agent_idx] = "#"
            else:
                line[agent_idx] = "A"
                line[reward_idx] = "R"
            print("".join(line))

            # stats
            print(f"Agent Pos: {agentPosition:.1f}, Reward Pos: {rewardPosition:.1f}, Distance: {distance:.1f}")
            print(f"Precision: {precision:.2f}%, Time: {t}/{timeLimit}, Episode: {episode}/{episodeNum}")
            print(f"State: {stateNext}")
            
            # Q table visualizer
            print("\nQ Table (best action per state):")
            for s, actions in Q.items():
                best_action = max(actions, key=actions.get)
                print(f"{s}: {best_action} -> {actions}")

            playtime += 1
            time.sleep(1 / fps)

input("Finished. Press Enter to exit.")