import mcpi.minecraft as minecraft
import mcpi.block as block
import time

# minecraftstuff is a module built by Martin O'hanlon
# Download minecraft stuff from here:
# https://raw.githubusercontent.com/martinohanlon/minecraft-stuff/master/minecraftstuff.py
# Put a copy of it in the folder with this script.
import minecraftstuff as minecraftstuff

mc = minecraft.Minecraft.create()

# initialize the drawing module
mcd = minecraftstuff.MinecraftDrawing(mc)

# current player position
pos = mc.player.getTilePos()

"""
Room is created by making one sphere of the chosen material,
then hollowing it out by making a sphere of air that is 1 block
smaller than the first sphere.

ARGS:
  x, y, z - center point of the outside sphere
  r - radius of the outside sphere
  block - desired material id
"""
def make_room_at_pos (x, y, z, r, block):
    # outside sphere
    mcd.drawSphere(x, y, z, r, block)
    # inside sphere (air)
    mcd.drawSphere(x, y, z, r-1, 0)


"""
Make a room using the players current position as the center point.
Useful when playing interactively with python shell.

ARGS:
  block - desired material id
  r - radius of the outside sphere default 6
"""
def make_room(block, r=6):
    pos = mc.player.getTilePos()
    make_room_at_pos(pos.x, pos.y, pos.z, r, block)


"""
Make a tunnel using the supplied points as the ends.

Tunnel is created by finding all of the points along a straight line
between point1 and point2 then looping over each point and making
a sphere centered on the point, followed by hollowing it out with
air blocks.

ARGS:
  point1, point2 - The two end points of the straight line that the tunnel
                   follows.
  block - desired material id
  outside_r - outside radius of the tunnel
  inside_r - inside radius of the tunnel
"""
def make_tunnel_from_points(point1, point2, block, outside_r=4, inside_r=3):

    # get the points that represent the center line.
    line_pts = mcd.getLine(
         point1.x, point1.y, point1.z,
         point2.x, point2.y, point2.z
    )

    # loop over the line points and make a sphere centered on each point
    for pt in line_pts:
        mcd.drawSphere(pt.x, pt.y, pt.z, outside_r,block)

    # loop over each point again and make a sphere of air centered on each point.
    for pt in line_pts:
        mcd.drawSphere(pt.x, pt.y, pt.z, inside_r, 0)

"""
Make a tunnel by using the sword right click to define each of the two
input points. Useful for playing in interactive python shell.

Execute this method then equip a sword and right click a point, then
move somewhere else and right click another point.

ARGS:
  block - desired material id
  r - outside radius of the tunnel.
"""
def make_tunnel(block, r=4):
    # list variable to store the selected points
    points = []
    
    # number variable to store how many hits so far.
    hits = 0
    try:
        # infinite loop to wait for point selection hits.
        while True:
            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # if a block has been hit
            if blockHits:
                # for each block that has been hit
                for blockHit in blockHits:
                    #print (blockHit)

                    # if its the first hit.
                    if hits == 0:
                        # save the point in our list variable
                        points.append(minecraft.Vec3(blockHit.pos.x,
                                                     blockHit.pos.y,
                                                     blockHit.pos.z))
                        mc.postToChat("first point saved")

                    # if it's the second hit
                    elif hits == 1:
                        # save the point in our list variable
                        points.append(minecraft.Vec3(blockHit.pos.x,
                                                     blockHit.pos.y,
                                                     blockHit.pos.z))
                        mc.postToChat("building tunnel")

                        # Pass the two points plus the block and radius parameters
                        # into the make_tunnel_from_points() method.
                        make_tunnel_from_points(points[0],
                                                points[1],
                                                block,
                                                outside_r=r,
                                                inside_r=r-1)
                        
                        return # break out of the infinite loop.
                    
                # increase hits counter so we know which hit is first,
                # and which is second.
                hits += 1
                
            #sleep for a short time, this makes it easier on the CPU
            time.sleep(0.1)
            
    # break out of user press ctrl-c
    except KeyboardInterrupt:
        print("stopped")
    return

if __name__ == "__main__":
    print (pos)
    #make_tunnel((20, 1), r=3)
