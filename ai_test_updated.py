#사용할 라이브러리 불러오기
import cv2
import numpy as np
from tensorflow.keras.models import load_model

#함수 predi() : 예측

def predi():
    #모델 불러오기
    model = load_model('model.h5')

    #예측할 이미지 불러오기
    im = cv2.imread("check2.png")

    #흑백처리
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    #이진화
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)

    #이진화된 이미지에서 윤곽선 검출
    ctrs, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #rects에 좌표들 저장
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]

    #bounding box 이미지에 표시 및 bounding box들 안의 이미지를 예측 후 이미지 위에 표시
    for rect in rects:
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        leng = int(rect[3] * 1.4)
        pt1 = max(0, int(rect[1] + rect[3] // 2 - leng // 2))
        pt2 = max(0, int(rect[0] + rect[2] // 2 - leng // 2))
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]

        if roi.size != 0:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = roi.astype('float32') / 255.0  # 스케일링
            roi = np.expand_dims(roi, axis=-1)  # 채널 추가
            roi = np.expand_dims(roi, axis=0)   
            nbr = model.predict(roi)
            cv2.putText(im, str(np.argmax(nbr[0])), (rect[0], rect[1]), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3) #검출한 숫자 표시

    #인식 결과 출력
    cv2.imshow("Resulting Image with Rectangular ROIs", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    predi()