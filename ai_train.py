#라이브러리 호출
from numpy import unique
from tensorflow.keras.datasets.mnist import load_data
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D,MaxPool2D,Flatten,Dropout

#mnist 데이터 불러오기
(x_train, y_train),(x_test,y_test) = load_data()

#불러온 데이터 훈련과 테스트 용으로 나누기
x_train = x_train.reshape((x_train.shape[0],x_train.shape[1],x_train.shape[2],1))
x_test = x_test.reshape((x_test.shape[0],x_test.shape[1],x_test.shape[2],1))

in_shape = x_train.shape[1:]

#클래스의 수
n_classes = len(unique(y_train)); print(in_shape,n_classes)

#데이터를 0~1 사이의 수로 정규화
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

#cnn 모델 구축(vggnet의 일부 사용함)
model = Sequential()
model.add(Conv2D(32,(3,3),activation='relu',kernel_initializer='he_uniform',input_shape=in_shape))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(64,(3,3),activation='relu',kernel_initializer='he_uniform',input_shape=in_shape))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(64,(3,3),activation='relu',kernel_initializer='he_uniform',input_shape=in_shape))
model.add(MaxPool2D((2,2)))
model.add(Flatten())
model.add(Dense(100,activation='relu',kernel_initializer='he_uniform'))
model.add(Dropout(0.5)) #과적합 피하기 위해 추가
model.add(Dense(n_classes,activation='softmax'))

#모델 컴파일
model.compile(optimizer = 'adam',loss = 'sparse_categorical_crossentropy',metrics = ['accuracy'])
model.summary()

#학습
model.fit(x_train,y_train,epochs=10,batch_size=128,verbose=1)

#학습된 모델 평가 
loss,acc=model.evaluate(x_test,y_test,verbose=1)
print('Accuracy: %.3f' % acc)

#훈련한 모델 저장
model.save('model.h5')