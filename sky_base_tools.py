import mcpi.minecraft as minecraft
import mcpi.block as block
import mcpi.minecraftstuff as minecraftstuff
import time

mc = minecraft.Minecraft.create()
mcd = minecraftstuff.MinecraftDrawing(mc)
pos = mc.player.getTilePos()

def make_room_at_pos (x, y, z, r, block):
    mcd.drawSphere(x, y, z, r, block)
    mcd.drawSphere(x, y, z, r-1, 0)

def make_tunnel_from_points(point1, point2, block, outside_r=4, inside_r=3):
    line_pts = mcd.getLine(point1.x, point1.y, point1.z,
             point2.x, point2.y, point2.z)

    for pt in line_pts:
        mcd.drawSphere(pt.x, pt.y, pt.z, outside_r,block)


    for pt in line_pts:
        mcd.drawSphere(pt.x, pt.y, pt.z, inside_r, 0)

def make_room(block, r=6):
    pos = mc.player.getTilePos()
    make_room_at_pos(pos.x, pos.y, pos.z, r, block)

def make_tunnel(block, r=4):
    points = []
    hits = 0
    try:
        while True:
            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # if a block has been hit
            if blockHits:

                # for each block that has been hit
                for blockHit in blockHits:
                    #print (blockHit)
                    if hits == 0:
                        points.append(minecraft.Vec3(blockHit.pos.x,
                                                     blockHit.pos.y,
                                                     blockHit.pos.z))
                        mc.postToChat("first point saved")
                    elif hits == 1:
                        points.append(minecraft.Vec3(blockHit.pos.x,
                                                     blockHit.pos.y,
                                                     blockHit.pos.z))
                        mc.postToChat("building tunnel")
                        make_tunnel_from_points(points[0], points[1], block, outside_r=r, inside_r=r-1)
                        return
                hits += 1
            #sleep for a short time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("stopped")
    return

if __name__ == "__main__":

    print (pos)
    #make_room(pos.x, pos.y + 4, pos.z, 8, (95, 11))
