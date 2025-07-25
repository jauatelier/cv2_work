import numpy as np
import cv2

# 이미지 파일 읽기
src = cv2.imread("origin.png")
if src is None:
    print("origin.png 파일을 찾을 수 없습니다.")
    exit()

# BGR → HSV 변환
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

# 파란색 HSV 범위 정의
lower_blue = np.array([100, 100, 120])
upper_blue = np.array([150, 255, 255])

# 파란색 마스크 생성 및 적용
mask = cv2.inRange(hsv, lower_blue, upper_blue)
res_blue = cv2.bitwise_and(src, src, mask=mask)

# 파란색 객체 윤곽선 검출
gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
_, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

largest_contour = None
largest_area = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > largest_area:
        largest_area = area
        largest_contour = cnt

# 가장 큰 객체에 초록색 박스 그리기
if largest_contour is not None and largest_area > 500:
    x, y, width, height = cv2.boundingRect(largest_contour)
    cv2.rectangle(src, (x, y), (x + width, y + height), (0, 255, 0), 2)
    center_x = x + width // 2
    center_y = y + height // 2
    print("center: (%d, %d)" % (center_x, center_y))

# 결과 출력
cv2.imshow("Original + Bounding Box", src)
cv2.imshow("Blue Extracted", res_blue)

# 파란색 추출 영역 저장
cv2.imwrite("blue.png", res_blue)

# 종료 대기
print("ESC 키를 누르면 종료됩니다.")
while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

