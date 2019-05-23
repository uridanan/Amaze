#
# # The challenge
# # The challenge, shall you choose to accept it, is to develop until the 17.5.2019 23:59 Israel time a piece of software that does that: receives a level from Amaze and find the shortest solution possible or declare that this level has no solution.
# #
# # The program should assume handling levels to which the shortest solution is up to 100 steps.
# #
# # When executing the program it should not take more than 5 minutes per level on a standard computer.
# #
# # You will receive a list of XML files (attached here). Each file represents a level.
# #
# # Here’s an example of how the input is structured and the code would look like:
#
#
# # Filename, Time, S1, S2, S3…. Sn
# #
# # Where -
# #
# # Filename - the name of the file for this solution
# #
# # Time - the time, in seconds, it took to compute the level solution.
# #
# # Sn - The sequence of operations to complete the level - 1= right, 2= left, 3= up, 4= down.
#
#
# An Amaze!ng Coding Competition 🌟
# If you like programming, algorithms, challenges, competitions and $3,000 worth prize then this is for you!
#
# We’re looking for a software program that can find Amaze! Levels’ shortest solution.
#
# The challenge
# The challenge, shall you choose to accept it, is to develop until the 17.5.2019 23:59 Israel time a piece of software that does that: receives a level from Amaze and find the shortest solution possible or declare that this level has no solution.
#
# The program should assume handling levels to which the shortest solution is up to 100 steps.
#
# When executing the program it should not take more than 5 minutes per level on a standard computer.
#
# You will receive a list of XML files (attached here). Each file represents a level.
#
# Here’s an example of how the input is structured and the code would look like:
#
#
#
# <?xml version="1.0" encoding="UTF-8"?>
#
# <map version="1.2" tiledversion="1.2.2" orientation="orthogonal" renderorder="right-down" width="7" height="7" tilewidth="40" tileheight="40" infinite="0" nextlayerid="2" nextobjectid="1">
#
# <tileset firstgid="1" source="40.tsx"/>
#
# <layer id="1" name="Tile Layer 1" width="7" height="7">
#
#  <data encoding="csv">
#
# 0,0,0,0,0,0,0,
#
# 0,1,1,1,1,1,0,
#
# 0,1,0,0,0,1,0,
#
# 0,1,0,1,0,1,0,
#
# 0,1,0,1,0,1,0,
#
# 0,1,0,1,1,1,0,
#
# 0,0,0,0,0,0,0
#
# </data>
#
# </layer>
#
# </map>
#
#
# data - a list of integers with comma delimited. 0 value represents a wall. 1 or 2 is a free square.
#
# width, height - the level matrix dimensions
#
# The ball position is always positioned in the first free leftmost place. In the above example, it is colored in red.
#
#
#
# /*
#
# * An example representation of a level in the game
#
# */
#
# Class Level {
#
#     //0=white square 1=black square.
#
#     //The ball moves on black squares
#
#     int[][] squares;
#
#     int ballXStartLocation;
#
#     int ballYStartLocation;
#
# }
#
# /*
#
# * This is the main method that receives a Level and returns
#
# * a solution with the minimal number of steps to this level
#
# * in the form of array of movements.
#
# * The method should return null if the level is non solveable
#
# * 1 = right, 2= left, 3 = up, 4 = down
#
# */
#
# static int[] shortestSolution(Level level){
#
#     //Do your magic here
#
# }
#
#
# How to deliver your solution
# Once you are complete and sure about your solution you should submit a link to GitHub public repository which includes your code. You should also provide a file of solved levels in the following format (one line for each level):
#
#
# Filename, Time, S1, S2, S3…. Sn
#
# Where -
#
# Filename - the name of the file for this solution
#
# Time - the time, in seconds, it took to compute the level solution.
#
# Sn - The sequence of operations to complete the level - 1= right, 2= left, 3= up, 4= down.
#
#
# * note - this file will be tested automatically so it is important that you will deliver in the correct format.
#
#
# Your code will be re-executed by us on a personal desktop to validate the solution and to have a fair performance comparison between solutions.
#
# You can code in any of the following languages: Java, Javascript, Python2/3, C/C++, C#, Go.
#
# If you wish to code it in any other language please consult first with Eran Heres (eranh@tabtale.com).
#
# Your code should include all external dependencies and instructions on how to execute it in the README.md file.
#
#
# The Prize
# The winner receives a couple’s vacation to wherever she chooses, worth up to $3,000, including up to 3 vacation days at the company expense.
#
# Winner
# The winner is selected in the following way:
#
# The solution must work on 100% of the levels.
#
# The solution must identify unresolvable levels.
#
# Your solution must provide the shortest path compared to other solutions.
#
# If there’s more than one solver, the fastest solution when executed on the same computer for the first Amaze! 170 levels wins.
#
# If by a miracle 2 people gave the same solution, the one that submitted it earlier wins.
#
#
# Other Rules
# The competition is for TabTale employees only (by 1.8.2019).
#
# Working on the solution must not be done during work hours.