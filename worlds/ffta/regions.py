from BaseClasses import Entrance, ItemClassification, Region, Location

from .data import FFTAData
from .items import FFTAItem
from .locations import FFTALocations, FFTALocation, MissionGroups, FFTALocationData, DispatchMissionGroups

#FFTAValidLocations = []
#FFTALocationGroup = []
#gates = []
#valid_gates = []


def create_gates(num_gate: int, gate: Region, world, last_gate: bool, FFTAValidLocations, FFTAValidDispatch, dispatch_gate: Region, last_dispatch_gate: bool):

    if last_gate:
        world.multiworld.regions.append(gate)
        location_index = (num_gate - 1) * world.options.mission_reward_num.value * 4 + world.options.mission_reward_num.value * 3
        for i in range(world.options.mission_reward_num.value):
            gate.locations.append(FFTAValidLocations[location_index + i])
            FFTAValidLocations[location_index + i].parent_region = gate
        
        if world.options.gate_items.value == 2:
            if last_dispatch_gate:
                dispatch_index = (num_gate - 1) * world.options.mission_reward_num.value * world.options.dispatch.value + world.options.mission_reward_num.value * (world.options.dispatch.value - 1)
                for j in range(world.options.mission_reward_num.value):
                    index = dispatch_index + j
                    dispatch_gate.locations.append(FFTAValidDispatch[index])
                    FFTAValidDispatch[index].parent_region = dispatch_gate
            #else:
            #    num_dispatch = world.options.mission_reward_num.value * world.options.dispatch.value
            #    dispatch_index = (num_gate - 1) * num_dispatch + world.options.mission_reward_num.value * (world.options.dispatch.value - 1)
            #    for j in range(num_dispatch):
            #        index = dispatch_index + j
            #        dispatch_gate.locations.append(FFTAValidDispatch[index])
            #        FFTAValidDispatch[index].parent_region = dispatch_gate
        return
    
    num_missions: int
    num_dispatch: int

    if num_gate == 0:
        num_missions = world.options.mission_reward_num.value * 3
        location_index = 0

    else:
        num_missions = world.options.mission_reward_num.value * 4
        location_index = (num_gate - 1) * num_missions + world.options.mission_reward_num.value * 3

    if world.options.gate_items.value == 2:
        if num_gate == 0:
            num_dispatch = world.options.mission_reward_num.value * (world.options.dispatch.value - 1)
            dispatch_index = 0
        else:
            num_dispatch = world.options.mission_reward_num.value * world.options.dispatch.value
            dispatch_index = (num_gate - 1) * num_dispatch + world.options.mission_reward_num.value * (world.options.dispatch.value - 1)
    else:
        num_dispatch = world.options.mission_reward_num.value * world.options.dispatch.value
        dispatch_index = num_gate * num_dispatch
    
    world.multiworld.regions.append(gate)

    # Add dispatch gate regions if option is selected
    if world.options.gate_items.value == 2:
        world.multiworld.regions.append(dispatch_gate)

    for i in range(num_missions):
        index = location_index + i
        gate.locations.append(FFTAValidLocations[index])
        FFTAValidLocations[index].parent_region = gate

    if world.options.gate_items.value == 2:
        for j in range(num_dispatch):
            index = dispatch_index + j
            dispatch_gate.locations.append(FFTAValidDispatch[index])
            FFTAValidDispatch[index].parent_region = dispatch_gate

    else:
        for j in range(num_dispatch):
            index = dispatch_index + j
            gate.locations.append(FFTAValidDispatch[index])
            FFTAValidDispatch[index].parent_region = gate


def create_regions(world, player) -> None:

    FFTAValidLocations = []
    FFTAValidDispatch = []
    gates = []
    dispatch_gates = []
    valid_gates = []
    valid_dispatch = []
    TotemaLocations = []
    StoryLocations = []

    # Setting number of locations per mission
    world.MissionGroups = []
    ActualMissionGroups = MissionGroups.copy()
    for i, missionGroup in enumerate(ActualMissionGroups):
        ActualMissionGroups[i] = (missionGroup[0][0:world.options.mission_reward_num.value], missionGroup[1], missionGroup[2])
    world.MissionGroups = ActualMissionGroups

    # Setting number of locations per dispatch mission
    world.DispatchMissionGroups = []
    ActualDispatchMissionGroups = DispatchMissionGroups.copy()
    for i, missionGroup in enumerate(ActualDispatchMissionGroups):
        ActualDispatchMissionGroups[i] = (missionGroup[0][0:world.options.mission_reward_num.value], missionGroup[1], missionGroup[2])
    world.DispatchMissionGroups = ActualDispatchMissionGroups

    menu_region = Region("Menu", player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    #for location in FFTALocations:
    #    location = FFTALocation(player, location.name, location.rom_address)
    #   FFTAValidLocations.append(location)

    # Adding totema missions to list and deleting them from mission groups
    if world.options.final_unlock.value == 1:
        for location in world.MissionGroups[4][0]:
            TotemaLocations.append(FFTALocation(player, location.name, location.rom_address))

        del world.MissionGroups[4]

        for location in world.MissionGroups[6][0]:
            TotemaLocations.append(FFTALocation(player, location.name, location.rom_address))

        del world.MissionGroups[6]

        for location in world.MissionGroups[8][0]:
            TotemaLocations.append(FFTALocation(player, location.name, location.rom_address))

        del world.MissionGroups[8]

        for location in world.MissionGroups[11][0]:
            TotemaLocations.append(FFTALocation(player, location.name, location.rom_address))

        del world.MissionGroups[11]

        for location in world.MissionGroups[13][0]:
            TotemaLocations.append(FFTALocation(player, location.name, location.rom_address))

        del world.MissionGroups[13]

    # Having the story missions be the gate unlocks and removing them from the mission pool.
    if world.options.mission_order.value == 1:

        end_range = 23

        # Account for the removed totema missions if that option is selected
        if world.options.final_unlock.value == 1:
            end_range = 17

        for index in range(0, end_range):
            StoryLocations.append(world.MissionGroups[0])
            del world.MissionGroups[0]

    if world.options.mission_order.value == 1 or world.options.mission_order.value == 2:
        world.random.shuffle(world.MissionGroups)

    # Randomize dispatch missions if the option is set to true
    if world.options.randomize_dispatch.value == 1:
        world.random.shuffle(world.DispatchMissionGroups)

    # Insert story missions on every fourth mission to be the requirement mission
    if world.options.mission_order.value == 1:
        story_index = 0
        i = 3
        for gate in range(world.options.gate_num.value):
            while i < len(world.MissionGroups) and story_index < len(StoryLocations):
                world.MissionGroups.insert(i, StoryLocations[story_index])
                i = i + 4
                story_index = story_index + 1

    # Adding missions to valid locations to create the locations
    for index, mission in enumerate(world.MissionGroups):
        for reward in mission[0]:
            reward_location = FFTALocation(player, reward.name, reward.rom_address)
            FFTAValidLocations.append(reward_location)
        
    # Add the dispatch missions
    #world.random.shuffle(world.DispatchMissionGroups)
    for index, mission in enumerate(world.DispatchMissionGroups):
        for reward in mission[0]:
            reward_location = FFTALocation(player, reward.name, reward.rom_address)
            FFTAValidDispatch.append(reward_location)

    #for index, mission in enumerate(FFTAValidLocations):
    #    print("This is the locations in valid locations in order: " + mission.name)


    # Create region gates
    gate_1 = Region("Gate 1", player, world.multiworld)
    gate_2 = Region("Gate 2", player, world.multiworld)
    gate_3 = Region("Gate 3", player, world.multiworld)
    gate_4 = Region("Gate 4", player, world.multiworld)
    gate_5 = Region("Gate 5", player, world.multiworld)
    gate_6 = Region("Gate 6", player, world.multiworld)
    gate_7 = Region("Gate 7", player, world.multiworld)
    gate_8 = Region("Gate 8", player, world.multiworld)
    gate_9 = Region("Gate 9", player, world.multiworld)
    gate_10 = Region("Gate 10", player, world.multiworld)
    gate_11 = Region("Gate 11", player, world.multiworld)
    gate_12 = Region("Gate 12", player, world.multiworld)
    gate_13 = Region("Gate 13", player, world.multiworld)
    gate_14 = Region("Gate 14", player, world.multiworld)
    gate_15 = Region("Gate 15", player, world.multiworld)
    gate_16 = Region("Gate 16", player, world.multiworld)
    gate_17 = Region("Gate 17", player, world.multiworld)
    gate_18 = Region("Gate 18", player, world.multiworld)
    gate_19 = Region("Gate 19", player, world.multiworld)
    gate_20 = Region("Gate 20", player, world.multiworld)
    gate_21 = Region("Gate 21", player, world.multiworld)
    gate_22 = Region("Gate 22", player, world.multiworld)
    gate_23 = Region("Gate 23", player, world.multiworld)
    gate_24 = Region("Gate 24", player, world.multiworld)
    gate_25 = Region("Gate 25", player, world.multiworld)
    gate_26 = Region("Gate 26", player, world.multiworld)
    gate_27 = Region("Gate 27", player, world.multiworld)
    gate_28 = Region("Gate 28", player, world.multiworld)
    gate_29 = Region("Gate 29", player, world.multiworld)
    gate_30 = Region("Gate 30", player, world.multiworld)
    gate_31 = Region("Gate 31", player, world.multiworld)
    gate_32 = Region("Gate 32", player, world.multiworld)
    gate_33 = Region("Gate 33", player, world.multiworld)

    dispatch_gate_1 = Region("Dispatch Gate 1", player, world.multiworld)
    dispatch_gate_2 = Region("Dispatch Gate 2", player, world.multiworld)
    dispatch_gate_3 = Region("Dispatch Gate 3", player, world.multiworld)
    dispatch_gate_4 = Region("Dispatch Gate 4", player, world.multiworld)
    dispatch_gate_5 = Region("Dispatch Gate 5", player, world.multiworld)
    dispatch_gate_6 = Region("Dispatch Gate 6", player, world.multiworld)
    dispatch_gate_7 = Region("Dispatch Gate 7", player, world.multiworld)
    dispatch_gate_8 = Region("Dispatch Gate 8", player, world.multiworld)
    dispatch_gate_9 = Region("Dispatch Gate 9", player, world.multiworld)
    dispatch_gate_10 = Region("Dispatch Gate 10", player, world.multiworld)
    dispatch_gate_11 = Region("Dispatch Gate 11", player, world.multiworld)
    dispatch_gate_12 = Region("Dispatch Gate 12", player, world.multiworld)
    dispatch_gate_13 = Region("Dispatch Gate 13", player, world.multiworld)
    dispatch_gate_14 = Region("Dispatch Gate 14", player, world.multiworld)
    dispatch_gate_15 = Region("Dispatch Gate 15", player, world.multiworld)
    dispatch_gate_16 = Region("Dispatch Gate 16", player, world.multiworld)
    dispatch_gate_17 = Region("Dispatch Gate 17", player, world.multiworld)
    dispatch_gate_18 = Region("Dispatch Gate 18", player, world.multiworld)
    dispatch_gate_19 = Region("Dispatch Gate 19", player, world.multiworld)
    dispatch_gate_20 = Region("Dispatch Gate 20", player, world.multiworld)
    dispatch_gate_21 = Region("Dispatch Gate 21", player, world.multiworld)
    dispatch_gate_22 = Region("Dispatch Gate 22", player, world.multiworld)
    dispatch_gate_23 = Region("Dispatch Gate 23", player, world.multiworld)
    dispatch_gate_24 = Region("Dispatch Gate 24", player, world.multiworld)
    dispatch_gate_25 = Region("Dispatch Gate 25", player, world.multiworld)
    dispatch_gate_26 = Region("Dispatch Gate 26", player, world.multiworld)
    dispatch_gate_27 = Region("Dispatch Gate 27", player, world.multiworld)
    dispatch_gate_28 = Region("Dispatch Gate 28", player, world.multiworld)
    dispatch_gate_29 = Region("Dispatch Gate 29", player, world.multiworld)
    dispatch_gate_30 = Region("Dispatch Gate 30", player, world.multiworld)
    dispatch_gate_31 = Region("Dispatch Gate 31", player, world.multiworld)
    dispatch_gate_32 = Region("Dispatch Gate 32", player, world.multiworld)
    dispatch_gate_33 = Region("Dispatch Gate 33", player, world.multiworld)

    final_mission = Region("Final Mission Gate", player, world.multiworld)
    path_completes = [
        Region("Path 1 Completion", player, world.multiworld),
        Region("Path 2 Completion", player, world.multiworld),
        Region("Path 3 Completion", player, world.multiworld),
    ]


    #Add these based on gate settings?
    gates.append(gate_1)
    gates.append(gate_2)
    gates.append(gate_3)
    gates.append(gate_4)
    gates.append(gate_5)
    gates.append(gate_6)
    gates.append(gate_7)
    gates.append(gate_8)
    gates.append(gate_9)
    gates.append(gate_10)
    gates.append(gate_11)
    gates.append(gate_12)
    gates.append(gate_13)
    gates.append(gate_14)
    gates.append(gate_15)
    gates.append(gate_16)
    gates.append(gate_17)
    gates.append(gate_18)
    gates.append(gate_19)
    gates.append(gate_20)
    gates.append(gate_21)
    gates.append(gate_22)
    gates.append(gate_23)
    gates.append(gate_24)
    gates.append(gate_25)
    gates.append(gate_26)
    gates.append(gate_27)
    gates.append(gate_28)
    gates.append(gate_29)
    gates.append(gate_30)
    gates.append(gate_31)
    gates.append(gate_32)
    gates.append(gate_33)

    # Dispatch mission gates
    dispatch_gates.append(dispatch_gate_1)
    dispatch_gates.append(dispatch_gate_2)
    dispatch_gates.append(dispatch_gate_3)
    dispatch_gates.append(dispatch_gate_4)
    dispatch_gates.append(dispatch_gate_5)
    dispatch_gates.append(dispatch_gate_6)
    dispatch_gates.append(dispatch_gate_7)
    dispatch_gates.append(dispatch_gate_8)
    dispatch_gates.append(dispatch_gate_9)
    dispatch_gates.append(dispatch_gate_10)
    dispatch_gates.append(dispatch_gate_11)
    dispatch_gates.append(dispatch_gate_12)
    dispatch_gates.append(dispatch_gate_13)
    dispatch_gates.append(dispatch_gate_14)
    dispatch_gates.append(dispatch_gate_15)
    dispatch_gates.append(dispatch_gate_16)
    dispatch_gates.append(dispatch_gate_17)
    dispatch_gates.append(dispatch_gate_18)
    dispatch_gates.append(dispatch_gate_19)
    dispatch_gates.append(dispatch_gate_20)
    dispatch_gates.append(dispatch_gate_21)
    dispatch_gates.append(dispatch_gate_22)
    dispatch_gates.append(dispatch_gate_23)
    dispatch_gates.append(dispatch_gate_24)
    dispatch_gates.append(dispatch_gate_25)
    dispatch_gates.append(dispatch_gate_26)
    dispatch_gates.append(dispatch_gate_27)
    dispatch_gates.append(dispatch_gate_28)
    dispatch_gates.append(dispatch_gate_29)
    dispatch_gates.append(dispatch_gate_30)
    dispatch_gates.append(dispatch_gate_31)
    dispatch_gates.append(dispatch_gate_32)
    dispatch_gates.append(dispatch_gate_33)

    if world.options.final_mission.value == 0:
        final_location = FFTALocation(player, 'Royal Valley', None)
    elif world.options.final_mission.value == 1:
        final_location = FFTALocation(player, 'Decision Time', None)

    final_mission.locations.append(final_location)
    final_location.parent_region = final_mission
    world.multiworld.regions.append(final_mission)

    gate_number = world.options.gate_num.value

    # Might need to change this to 29 for now because of removal of missions
    if gate_number > 30 and world.options.final_unlock.value == 1:
        gate_number = 30
    
    dispatch_gate_number = gate_number
    gate_number = gate_number + world.options.gate_paths.value - 1

    # Add number of gates based on settings
    for i in range(gate_number + 1):
        valid_gates.append(gates[i])

        if world.options.gate_items.value == 2 and i < dispatch_gate_number + 1:
            valid_dispatch.append(dispatch_gates[i])

    # look into adding gate_1.name?
    menu_region.connect(gate_1)

    if world.options.gate_items.value == 2:
        gate_1.connect(dispatch_gate_1)

    last_gate = False
    last_dispatch_gate = False
    if world.options.gate_paths.value == 1:
        for x in range(len(valid_gates)):
            if x == len(valid_gates) - 1:
                last_gate = True
                last_dispatch_gate = True

            if world.options.gate_items.value == 2:
                create_gates(x, valid_gates[x], world, last_gate, FFTAValidLocations, FFTAValidDispatch, valid_dispatch[x], last_dispatch_gate)

            else:
                create_gates(x, valid_gates[x], world, last_gate, FFTAValidLocations, FFTAValidDispatch, 0, last_dispatch_gate)

            if x > 0:
                valid_gates[x-1].connect(valid_gates[x], valid_gates[x].name)

                if world.options.gate_items.value == 2:
                    valid_dispatch[x - 1].connect(valid_dispatch[x], valid_dispatch[x].name)
    elif world.options.gate_paths.value > 1:

        for x in range(len(valid_gates)):
            if x == len(valid_gates) - world.options.gate_paths.value:
                last_gate = True
                last_dispatch_gate = True
            if world.options.gate_items.value == 2 and x >= len(valid_dispatch):
                last_dispatch_gate = False
                    
            if world.options.gate_items.value == 2 and x < len(valid_dispatch):
                create_gates(x, valid_gates[x], world, last_gate, FFTAValidLocations, FFTAValidDispatch, valid_dispatch[x], last_dispatch_gate)

            else:
                create_gates(x, valid_gates[x], world, last_gate, FFTAValidLocations, FFTAValidDispatch, 0, last_dispatch_gate)

            if world.options.gate_items.value == 2 and x > 0 and x < len(valid_dispatch):
                valid_dispatch[x - 1].connect(valid_dispatch[x], valid_dispatch[x].name)


        
        path_lengths = [0, 0, 0]
        for i in range(0, world.options.gate_paths.value):
            # Splitting gates into paths
            path = valid_gates[i+1::world.options.gate_paths.value]
            path_lengths[i] = len(path)

            gate_1.connect(path[0], path[0].name)
            for x in range(1, len(path)):
                path[x - 1].connect(path[x], path[x].name)

            path_complete_location = FFTALocation(player, f"Path {i+1} Completion", None)

            path_completes[i].locations.append(path_complete_location)
            path_complete_location.parent_region = path_completes[i]
            world.multiworld.regions.append(path_completes[i])
            
            path[-1].connect(path_completes[i], path_completes[i].name)
            
            # Connect the path finish events to the final mission
            path_completes[i].connect(final_mission, final_mission.name)

        # Setting the lengths of the paths
        world.path1_length = path_lengths[0]
        world.path2_length = path_lengths[1]
        world.path3_length = path_lengths[2]

    # Set up regions for totema unlock option
    if world.options.final_unlock.value == 1:
        totema1 = Region("Totema 1", player, world.multiworld)
        totema2 = Region("Totema 2", player, world.multiworld)
        totema3 = Region("Totema 3", player, world.multiworld)
        totema4 = Region("Totema 4", player, world.multiworld)
        totema5 = Region("Totema 5", player, world.multiworld)

        world.multiworld.regions.append(totema1)
        world.multiworld.regions.append(totema2)
        world.multiworld.regions.append(totema3)
        world.multiworld.regions.append(totema4)
        world.multiworld.regions.append(totema5)

        totema1.locations.append(TotemaLocations[0])
        totema1.locations.append(TotemaLocations[1])
        TotemaLocations[0].parent_region = totema1
        TotemaLocations[1].parent_region = totema1

        totema2.locations.append(TotemaLocations[2])
        totema2.locations.append(TotemaLocations[3])
        TotemaLocations[2].parent_region = totema2
        TotemaLocations[3].parent_region = totema2

        totema3.locations.append(TotemaLocations[4])
        totema3.locations.append(TotemaLocations[5])
        TotemaLocations[4].parent_region = totema3
        TotemaLocations[5].parent_region = totema3

        totema4.locations.append(TotemaLocations[6])
        totema4.locations.append(TotemaLocations[7])
        TotemaLocations[6].parent_region = totema4
        TotemaLocations[7].parent_region = totema4

        totema5.locations.append(TotemaLocations[8])
        totema5.locations.append(TotemaLocations[9])
        TotemaLocations[8].parent_region = totema5
        TotemaLocations[9].parent_region = totema5

        menu_region.connect(totema1, "Totema 1")
        totema1.connect(totema2, "Totema 2")
        totema2.connect(totema3, "Totema 3")
        totema3.connect(totema4, "Totema 4")
        totema4.connect(totema5, "Totema 5")
        totema5.connect(final_mission)

    # Set the final mission to connect to the last mission in the path
    if world.options.gate_paths.value == 1:
        # Always connect the last gate to the final mission for the mission gate goal
        valid_gates[gate_number].connect(final_mission)
