
import numpy as np
import cv2
import matplotlib.pyplot as plt





def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

class ball:
    def __init__(self,num,pos):
        self.num=num
        self.pos=pos



posHole=np.array([0,0,0])
posWhiteBall=np.array([100,50,0])
posBall=np.array([50,50,0])

def goStrike(posHole,posBall,posWhiteBall,ballRadius):
    '''
    input:
    Hole position np.array(3)
    Ball position np.array(3)
    White Ball position np.array(3)

    output:
    strike position np.array(3)
    strike vector np.array(3)

    '''
    # 球的大小
    radius=ballRadius # mm

    vecBall2Hole=posHole-posBall 
    vecnBall2Hole=normalize(vecBall2Hole)
    # need to add two radius

    posWhiteBallcollision=posBall-radius*2*vecnBall2Hole # 白球碰撞位置
    vecWhiteballStrike=posWhiteBallcollision-posWhiteBall # 白球碰撞向量(也就是擊打向量)
    vecnWhiteballStrike=normalize(vecWhiteballStrike)

    posStrike=posWhiteBall-radius*vecnWhiteballStrike # 白球擊打位置
    posintStrike=posStrike.astype(int)
    
    return posintStrike,vecWhiteballStrike


def drawTable(posHole,posWhiteBall,posBall,p1,v1,ballRadius):
    # 畫出圖
    shape=(960,1280,3)
    img = np.zeros(shape, np.uint8)

    # 畫洞
    cv2.circle(img,(posHole[0],posHole[1]),ballRadius,color=(255,255,0),thickness=4)

    # 畫球
    cv2.circle(img,(posBall[0],posBall[1]),ballRadius,color=(0,255,0),thickness=4)

    # 畫白球
    cv2.circle(img,(posWhiteBall[0],posWhiteBall[1]),ballRadius,color=(255,255,255),thickness=4)

    # 打擊方向
    cv2.line(img, (p1[0], p1[1]), ((int)(p1[0]-0.5*v1[0]), (int)(p1[1]-0.5*v1[1])), (0, 0, 255), 3)

    # 文字
    text = f'W:{posWhiteBall}'
    cv2.putText(img, text, (900, 150), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
    text = f'B:{posBall}'
    cv2.putText(img, text, (900, 180), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)
    text = f'H:{posHole}'
    cv2.putText(img, text, (900, 210), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

    text = f'out pos:{p1}'
    cv2.putText(img, text, (900, 250), cv2.FONT_HERSHEY_PLAIN,1, (255, 0, 255), 1, cv2.LINE_AA)
    text = f'out vec:{v1}'
    cv2.putText(img, text, (900, 280), cv2.FONT_HERSHEY_PLAIN,1, (255, 0, 255), 1, cv2.LINE_AA)

    # cv2.imshow("-",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    cv2.imwrite('collision.png', img)
    return

def drawball(balls,whiteball,hole,ballRadius):
    # 出圖
    shape=(960,1280,3)
    img = np.zeros(shape, np.uint8)

    # 畫洞
    for h in hole:
        cv2.circle(img,(h[0],h[1]),ballRadius,color=(255,255,0),thickness=4)

    # 畫球
    for b in balls:
        cv2.circle(img,(b.pos[0],b.pos[1]),ballRadius,color=(0,255,0),thickness=4)
        cv2.putText(img, b.num, (b.pos[0],b.pos[1]), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 255), 1, cv2.LINE_AA)

    # 畫白球
    for w in whiteball:
        cv2.circle(img,(w.pos[0],w.pos[1]),ballRadius,color=(255,255,255),thickness=4)
        cv2.putText(img, w.num, (w.pos[0],w.pos[1]), cv2.FONT_HERSHEY_PLAIN,1, (255,255,255), 1, cv2.LINE_AA)
    
    # cv2.imshow("-",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return

def takefirst(elem):
     return int(elem[0])
 
def getdata(points):
    data=points
    data.sort(key=takefirst, reverse=False)
    balls=[]
    whiteBall=[]
    for b in data:
        if b[0]=='0':
            whiteBall.append(ball(b[0],b[1]))
        else:
            balls.append(ball(b[0],b[1]))
    return whiteBall,balls

def gethole(pockets):
    # 1000*800
    data=pockets
    return data

def getTableEdge(holes):
    '''
    # TODO need to be fixed
    input:
    holes[]: maybe missed
    [(x1, y1), (x2, y2)...]
    
    output:
    p1: the point near img coord (0,0)
    '''
    # find six hole
    # 0|1|2
    # 3|4|5
    hole_fix=[0,0,0,0,0,0]
    for h in holes:
        if h[1]<960/2:
            if h[0]<1280/3:
                hole_fix[0]=h
            elif h[1]<1280*2/3:
                hole_fix[1]=h
            else:
                hole_fix[2]=h
        else:
            if h[0]<1280/3:
                hole_fix[3]=h
            elif h[1]<1280*2/3:
                hole_fix[4]=h
            else:
                hole_fix[5]=h
    for i,hole in enumerate(hole_fix):
        if hole==0:
            # TODO arent finished
            pass
    
    return hole_fix

    



def get_distance_from_point_to_line(point, line_point1, line_point2):
    # if line_point1 == line_point2:
    #     point_array = np.array(point )
    #     point1_array = np.array(line_point1)
    #     return np.linalg.norm(point_array -point1_array )
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance

def drawLines(img_ori,p1c,p2c,p1s1,p1s2,p2s1,p2s2):
    img=img_ori.copy()
    cv2.line(img, p1c, p2c, (0, 0, 255), 5)
    cv2.line(img, p1s1, p1s2, (0, 255, 255), 5)
    cv2.line(img, p2s1, p2s2, (255, 0, 255), 5)
    plt.imshow(img)
    plt.show()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return 

def obstacleOnPath(balls,posHole,posWhiteBall,posBall,ballRadius_img,img):
    '''
    Input:
    balls: array of all ball
    posHole:
    posWhiteBall:
    posBall:
    ballRadius:
    img: original image
    
    Output:
    True: have obstacle, need change path
    False: clear path
    '''
    # white -> ball
    radius=ballRadius_img # mm
    vecBall2Hole=posHole-posBall 
    vecnBall2Hole=normalize(vecBall2Hole)
    posWhiteBallcollision=posBall-radius*2*vecnBall2Hole # 白球碰撞位置
    
    p1c=posWhiteBall
    p2c=posWhiteBallcollision
    m=normalize(p2c-p1c)
    m_inv=np.array([m[1],-m[0]])
    p1s1=p1c+radius*(m_inv)
    p1s2=p1c+radius*(-m_inv)
    p2s1=p2c+radius*(m_inv)
    p2s2=p2c+radius*(-m_inv)
    # drawLines(img,(int(p1c[0]),int(p1c[1])),(int(p2c[0]),int(p2c[1])),(int(p1s1[0]),int(p1s1[1])),
    #           (int(p1s2[0]),int(p1s2[1])),(int(p2s1[0]),int(p2s1[1])),(int(p2s2[0]),int(p2s2[1])))
    
    pathLen=get_distance_from_point_to_line(p1c,p2s1,p2s2)
    for b in balls:
        if get_distance_from_point_to_line(b.pos,p1c,p2c)<=3*radius:
            if get_distance_from_point_to_line(b.pos,p1s1,p1s2)<(pathLen):
                if get_distance_from_point_to_line(b.pos,p2s1,p2s2)<(pathLen):
                    # print(f"[Detected obstacle] id={b.num}, pos=({b.pos})")
                    return True
    
    
    # ball -> hole

    p1c=posBall
    p2c=posHole
    m=normalize(posHole-posBall)
    m_inv=np.array([m[1],-m[0]])
    p1s1=p1c+radius*(m_inv)
    p1s2=p1c+radius*(-m_inv)
    p2s1=p2c+radius*(m_inv)
    p2s2=p2c+radius*(-m_inv)
    
    # drawLines(img,(int(p1c[0]),int(p1c[1])),(int(p2c[0]),int(p2c[1])),(int(p1s1[0]),int(p1s1[1])),
    #           (int(p1s2[0]),int(p1s2[1])),(int(p2s1[0]),int(p2s1[1])),(int(p2s2[0]),int(p2s2[1])))
    
    pathLen=get_distance_from_point_to_line(p1c,p2s1,p2s2)
    
    for b in balls:
        if get_distance_from_point_to_line(b.pos,p1c,p2c)<=3*radius:
            if get_distance_from_point_to_line(b.pos,p1s1,p1s2)<(pathLen):
                if get_distance_from_point_to_line(b.pos,p2s1,p2s2)<(pathLen):
                    # print(f"[Detected obstacle] id={b.num}, pos=({b.pos})")
                    return True
    
    # print("[Detected obstacle] No obstacle on path")
    return False
  
  
def findball(whiteBall,balls,holes,ballRadius,img):
    # [X]先照順序，之後再說
    # 先找適合的洞
    # 檢查路徑上有沒有障礙物，有的話換下一個球
    # 都沒有的話就取第一顆球然後打直線
    ballRadius_img=30
    posWhiteBall=np.array(whiteBall[0].pos)
    for b in balls:
        value=-1
        id=-1
        for i,h in enumerate(holes):
            # print(value,id)
            dot_value=np.dot(normalize(b.pos-posWhiteBall),normalize(np.array(h)-b.pos))
            # print(b.pos,np.array(h),dot_value)
            if dot_value>value:
                if dot_value>0.15: 
                    value=dot_value
                    id=i
        if id==-1:
            # print(f"[find_hole]: ball id={b.num}, can't find any suitable hole")
            continue
            
        else:
            if obstacleOnPath(balls,np.array([holes[id][0],holes[id][1]]),posWhiteBall,np.array([b.pos[0],b.pos[1]]),ballRadius_img,img):
                # print(f"[Find hole] found obstacle")
                continue
            else:
                print(f"[Find hole] find hole = {id}, hole position = ({holes[id]})")
                posHole=np.array(holes[id])
                posBall=b.pos
                return posHole,posBall,posWhiteBall
    
    print("[Find hole] set straight path")
    posBall=balls[0].pos
    posHole=posBall+(posBall-posWhiteBall)
    return posHole,posBall,posWhiteBall

def cal_collision(points, pockets,img):
    ballRadius=30 #mm
    
    whiteBall,balls=getdata(points)
    holes=gethole(pockets)
    # print(holes)
    drawball(balls,whiteBall,holes,ballRadius)

    # posHole=np.array([10,10,0])
    # posWhiteBall=np.array([30,150,0])
    # posBall=np.array([26,56,0])
    
    if balls and whiteBall:
        print("[Status] Striking...")
        posHole,posBall,posWhiteBall=findball(whiteBall,balls,holes,ballRadius,img)
        p1,v1=goStrike(posHole,posBall,posWhiteBall,ballRadius)
        drawTable(posHole,posWhiteBall,posBall,p1,v1,ballRadius)
    elif not whiteBall:
        print("[Status] Cannot find the white ball.")
    elif not balls:
        print("[Status] End of the game.")

    # p1,v1=goStrike(posHole,posBall,posWhiteBall,ballRadius)
    # drawTable(posHole,posWhiteBall,posBall,p1,v1,ballRadius)