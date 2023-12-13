# %%
import numpy as np
import cv2
# %%



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
    for b in data[0:5]:
        if b[0]=='0':
            whiteBall.append(ball(b[0],b[1]))
        else:
            balls.append(ball(b[0],b[1]))
    return whiteBall,balls

def gethole(pockets):
    # 1000*800
    data=pockets
    return data

def findball(whiteBall,balls,holes):
    # 先照順序，之後再說
    posBall=np.array(balls[0].pos)
    posWhiteBall=np.array(whiteBall[0].pos)
    # 看哪個洞比較好(單位向量內積)
    value=-1
    id=-1
    for i,h in enumerate(holes):
        print(value,id)
        if np.dot(normalize(posBall-posWhiteBall),normalize(np.array(h)-posBall))>value:
            value=np.dot(normalize(posBall-posWhiteBall),normalize(np.array(h)-posBall))
            id=i
    posHole=np.array(holes[id])
    return posHole,posBall,posWhiteBall

def cal_collision(points, pockets):
    ballRadius=30 #mm
    
    whiteBall,balls=getdata(points)
    holes=gethole(pockets)
    drawball(balls,whiteBall,holes,ballRadius)

    # posHole=np.array([10,10,0])
    # posWhiteBall=np.array([30,150,0])
    # posBall=np.array([26,56,0])
    
    if balls and whiteBall:
        print("[Status] Striking...")
        posHole,posBall,posWhiteBall=findball(whiteBall,balls,holes)
        p1,v1=goStrike(posHole,posBall,posWhiteBall,ballRadius)
        drawTable(posHole,posWhiteBall,posBall,p1,v1,ballRadius)
    elif not whiteBall:
        print("[Status] Cannot find the white ball.")
    elif not balls:
        print("[Status] End of the game.")

    # p1,v1=goStrike(posHole,posBall,posWhiteBall,ballRadius)
    # drawTable(posHole,posWhiteBall,posBall,p1,v1,ballRadius)