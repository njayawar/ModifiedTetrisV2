import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

import random

NUM_RUNS = 50

async def reset(dut):
    dut.reset.value = 1
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    dut.reset.value = 0


@cocotb.test()
async def test_tetris(dut):

    # Set clock and reset game
    cocotb.start_soon(Clock(dut.clock, 50, units="ns").start())
    await reset(dut)
    dut.inputs.value = 0
    score = 0

    # Start New Game
    dut.inputs.value = 2
    await RisingEdge(dut.clock)
    dut.inputs.value = 0
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)
    await RisingEdge(dut.clock)

    # Assert game start
    game_status = ((dut.outputs.value)) & 1
    assert game_status == 1

    for x in range(0, NUM_RUNS):
        print("Iteration", (x+1), "of", NUM_RUNS)
        # Get current bounce position
        currentBouncePos = ((dut.outputs.value) >> 1) & 7
        await Timer(1, units="ns")
        # Check column status of bounce position
        dut.inputs.value = currentBouncePos << 2
        await Timer(1, units="ns")
        currColStack = ((dut.outputs.value) >> 4) & 15

        # Drop into column
        dut.inputs.value = 1
        await RisingEdge(dut.clock)
        dut.inputs.value = 0
        await Timer(1, units="ns")
        print("Dropping at Col:", currentBouncePos)

        # Wait a random amount of time
        waitTime = random.randrange(40000, 1000000)
        print("Clock Periods Waiting:", waitTime)
        for x in range(0, waitTime):
            await RisingEdge(dut.clock)

        # Get new column status
        dut.inputs.value = currentBouncePos << 2
        await Timer(1, units="ns")
        newColStack = ((dut.outputs.value) >> 4) & 15

        # Read Score
        dut.inputs.value = 32
        await Timer(1, units="ns")
        newScore = ((dut.outputs.value) >> 4) & 255

        # Check validity
        print("Col:", currentBouncePos, "# Blocks Was:", currColStack, "Now:", newColStack)
        print("Score was:", score, "Now:", newScore)
        assert (newColStack == currColStack + 1) or (currColStack == 0 and newScore == score+1)

        # Print Current Board
        print("Board State:")
        colVals = [0] * 8
        for i in range(0, 8):
            dut.inputs.value = i << 2
            await Timer(1, units="ns")
            colVals[i] = ((dut.outputs.value) >> 4) & 15
        for j in range(0, 8):
            str = ""
            for k in colVals:
                if(k > (8-j-1)):
                    str += "X"
                else:
                    str += "-"
            print(str)
        game_status = ((dut.outputs.value)) & 1
        if(game_status == 1):
            print("GAME RUNNING")
        else:
            print("GAME STOPPED")
        dut.inputs.value = 32
        await Timer(1, units="ns")
        printScore = ((dut.outputs.value) >> 4) & 255
        print("Score:", printScore)


        # Check for finished game
        game_status = ((dut.outputs.value)) & 1
        if(newColStack == 8):
            assert game_status == 0
            # Start New Game
            dut.inputs.value = 2
            await RisingEdge(dut.clock)
            dut.inputs.value = 0
            await RisingEdge(dut.clock)
            await RisingEdge(dut.clock)
            await RisingEdge(dut.clock)
            game_status = ((dut.outputs.value)) & 1
            assert game_status == 1
        else:
            assert game_status == 1
            

        score = newScore
        print("------------------------------------------------")