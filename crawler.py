from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

# 수집한 리뷰 저장하는 리스트
reviews = []

# Idius 상품 페이지 접속
driver = webdriver.Chrome()
driver.get('https://www.idus.com/v2/product/1457a4bf-bece-4d9a-bff3-3312511c986e')
time.sleep(2)

def sort_by_latest():
    try:
        sort_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.CoreButton.BaseButtonText.body1-regular-small'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sort_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", sort_button)
        print("최신 순으로 정렬하였습니다.")
        time.sleep(2)  # 정렬 적용 대기
    except Exception as e:
        print(f"정렬 버튼 클릭 실패: {str(e)}")
        return False
    return True

def close_login_popup():
    try:
        # 로그인 팝업의 닫기 버튼 찾기 (X 버튼)
        close_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="close"]'))
        )
        driver.execute_script("arguments[0].click();", close_button)
        print("로그인 팝업을 닫았습니다.")
        time.sleep(1)
    except:
        # 팝업이 없으면 그냥 넘어감
        pass

# 리뷰 수집
def collect_reviews(num_pages):
    # 초기 최신순 정렬
    if not sort_by_latest():
        return
    
    for page in range(num_pages):
        print(f"\n=== {page + 1}페이지 수집 시작 ===")
        
        # 로그인 팝업 닫기
        close_login_popup()
        
        # 각 페이지에서 최신순 정렬 상태 확인 및 적용
        if page > 0:  # 첫 페이지는 이미 정렬되어 있으므로 스킵
            if not sort_by_latest():
                break
        
        # 리뷰 수집 코드
        review_elements = driver.find_elements(By.CLASS_NAME, 'ReviewListItem__review')
        print(f"현재 페이지 리뷰 요소 수: {len(review_elements)}")
        
        for review in review_elements:
            try:
                review_text = review.find_element(By.CLASS_NAME, 'whitespace-pre-line.body1-regular-medium.line-clamp-6').text
                reviews.append(review_text)
                print(f"리뷰 수집됨: {len(reviews)}번째")
            except Exception as e:
                print(f"리뷰 수집 실패: {str(e)}")
                continue
        
        # 다음 페이지 이동
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.CoreButton.BaseButtonIcon.BasePagination__arrow.ml-\\[8px\\]'))
            )
            
            if not 'CoreButton--disabled' in next_button.get_attribute('class'):
                print("다음 페이지 버튼을 찾았습니다.")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)
                print(f"{page + 2}페이지로 이동 시도")
                time.sleep(2)
                
                # 페이지 이동 후 로그인 팝업 닫기
                close_login_popup()
            else:
                print("다음 페이지 버튼이 비활성화 상태입니다.")
                break
                
        except Exception as e:
            print(f"다음 페이지 이동 실패: {str(e)}")
            break

    # 수집된 리뷰를 JSON 파일로 저장
    with open('test_review.json', 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
    print("리뷰가 reviews.json 파일에 저장되었습니다.")

# 일부 페이지 (5페이지까지) 수집 (전체 페이지번호 : 846)
collect_reviews(5)

# 수집된 리뷰 확인
print(f'\n전체 수집된 리뷰 수: {len(reviews)}')
for i, review in enumerate(reviews[:40]):
    print(f'\n리뷰 {i+1}:', review)

# 종료
driver.quit()