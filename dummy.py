import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

if __name__ == '__main__':
    
  class VideoTransformer(VideoTransformerBase):
      def __init__(self):
          self.threshold1 = 100
          self.threshold2 = 200

      def transform(self, frame):
          img = frame.to_ndarray(format="bgr24")

          if self.click:
            cv2.imwrite('image_capture.jpg', img)

          return img


  ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

  if ctx.video_transformer:
      ctx.video_transformer.click = st.button("Capture")