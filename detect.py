import cv2
# import mediapipe as mp
import threading
import os
import PIL.Image, PIL.ImageTk
import playsound
import main, Health # class 가져 오기

from tkinter import *
from PIL import ImageTk, Image
# import ai 
from database import Graph
import time
result_value = []

class AI:
    def __init__(self, canvas, root, cam_panel):
        self.result = None
        self.canvas = canvas
        self.root = root
        self.cam_panel = cam_panel
        self.now_time = 0
    def create_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"폴더를 만들었습니다.: {folder_path}")
        else:
            print(f"폴더 존재 : {folder_path}")

    def neck_angle_value(self):
        global result_value
        # 측정 시작 쓰레드 작동
        thread = threading.Thread(target=self.music)
        thread.daemon = True
        thread.start()
         
        self.main()
        
        #print(f"neck_angle_value : {self.result}")
        
    def music(self):
        #측정 시작 음성
        filename = './mpfile/checking.mp3'
        playsound.playsound(filename)
    
    def music2(self):
        #측정 성공 음성
        filename = './mpfile/finish_checking.mp3'
        playsound.playsound(filename)
        
    def music3(self):
        #측정 실패시 음성
        filename = './mpfile/fail.mp3'
        playsound.playsound(filename)
    def gstreamer_pipeline(
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=60,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )
    def update_cam(self):
        #cap = cv2.VideoCapture(0)
        print(self.gstreamer_pipeline(flip_method=0))
        cap = cv2.VideoCapture(self.gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        if cap.isOpened():
            window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # cap = cv2.VideoCapture(0)
        
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(width, height)
        self.create_folder('Result/')

        count = 0
        check_value=[]
        print("측정")
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret, frame = cap.read()

            if not ret:
                break
            ori_frame = frame.copy()
            
            try:
                count += 1
                if count == 200:
                    cv2.imwrite('Result/UserPicture.jpeg', ori_frame)

                if cv2.waitKey(0) == 27 or count == 200: # 여기가 수정부분
                    self.now_time =0
                    # self.result = test__1()
                    """
                    model = ai.Detect('Result/UserPicture.jpeg')
                    check_value = model.get_coordinates()
                    values = model.combine_coordinates()
                    print(values) # x y 좌표
                    print('결과 측정 성공시')
                    
                    ex_value, ey_value, nx_value, ny_value = values
                    x = abs(ex_value - nx_value)
                    y = ny_value - ey_value
                    result = y/x
                    """
                    #print(result)
                    check_value=[1]
                    check_value.index(1)
                    check_value.index(2)
                    check_value.index(3)
                    
                    break
                #cv2.imshow('Main', frame)
                
                src = cv2.resize(frame, (950, 530))
                image = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
                image = PIL.Image.fromarray(image)
                imgtk = PIL.ImageTk.PhotoImage(image=image)
                self.cam_panel.config(image=imgtk,width=950,height=530)
                self.cam_panel.image = imgtk
                origin_frame = frame.copy()
                
                if cv2.waitKey(0) == 27:
                    break
            except Exception as e:
                print(e)
                thread = threading.Thread(target=self.music3)
                thread.daemon = True
                thread.start()
                
                print("측정에 실패하였습니다(update_cam 함수)")
                cap.release()
                self.black_img = Image.open("img/1B1B1B.png")
                self.black_img = self.black_img.resize((1050, 1200))
                self.root.black_img = ImageTk.PhotoImage(self.black_img)
                self.star_button = Label(self.root,image=self.root.black_img,width=1050,height=1200, bg="white",borderwidth=0, 
                                        highlightthickness=0)
                self.canvas.create_window(540, 1000, window=self.star_button)
                main.main_menu(self.canvas, self.root)
                cap.release()

                return 11
        # 사람, 귀, 경추가 모두 측정이 되었을 경우
        
        thread = threading.Thread(target=self.music2)
        thread.daemon = True
        thread.start()
        
        cap.release()
        cv2.destroyAllWindows()
        
        self.black_img = Image.open("img/1B1B1B.png")
        self.black_img = self.black_img.resize((1050, 1200))
        self.root.black_img = ImageTk.PhotoImage(self.black_img)

        self.star_button = Label(self.root,image=self.root.black_img,width=1050,height=1200, bg="white",borderwidth=0, highlightthickness=0)

        self.canvas.create_window(540, 1000, window=self.star_button)
        Health.HealthList(self.canvas, self.root)
        return 1
        
    def main(self):
        thread = threading.Thread(target=self.update_cam)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    root = Tk()  # Tk 생성
    # root.overrideredirect(True)
    canvas = Canvas(root, bg="#1b1b1b")
    
    canvas.pack(fill=BOTH, expand=TRUE)
    
    root.geometry("1100x570")
    
    cam_panel = Label(root,text="카메라 준비중...",font=('NanumGothic', 30),width=40,height=12, bg="white",
                               borderwidth=0, anchor='center',highlightthickness=0)
    canvas.create_window(550, 285, window=cam_panel)
    
    result_value = AI(canvas, root, cam_panel).neck_angle_value()
    
    
    print("result_value", result_value)
    root.mainloop()
  
    

    