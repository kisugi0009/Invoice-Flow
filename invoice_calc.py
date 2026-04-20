import streamlit as st

st.set_page_config(page_title="發票小幫手", layout="centered")

# 自定義大寫轉換函數 (手寫三聯式發票必備)
def to_chinese_num(n):
    if n == 0: return "零"
    units = ["", "拾", "佰", "仟", "萬", "拾", "佰", "仟", "億"]
    nums = "零壹貳參肆伍陸柒捌玖"
    res = ""
    for i, digit in enumerate(reversed(str(int(n)))):
        if digit != '0':
            res = nums[int(digit)] + units[i] + res
        else:
            if not res.startswith("零"):
                res = "零" + res
    return res.rstrip("零") + "元整"

st.title("⚖️ 三聯式發票計算機")

# --- 輸入區 ---
with st.container():
    mode = st.radio("選擇計算模式", ["未稅 ⮕ 含稅 (5%外加)", "含稅 ⮕ 未稅 (5%內含)"], horizontal=True)
    amount = st.number_input("請輸入金額", min_value=0, step=1, value=0)

# --- 核心計算 ---
if mode == "未稅 ⮕ 含稅 (5%外加)":
    sales_amount = amount
    tax = round(sales_amount * 0.05)
    total_amount = sales_amount + tax
else:
    total_amount = amount
    sales_amount = round(total_amount / 1.05)
    tax = total_amount - sales_amount

# --- 顯示區 ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("銷售額 (未稅)", f"{sales_amount:,}")
c2.metric("營業稅", f"{tax:,}")
c3.metric("總計 (含稅)", f"{total_amount:,}")

# --- 手寫輔助 ---
if total_amount > 0:
    st.success(f"**金額大寫：** {to_chinese_num(total_amount)}")
    
    with st.expander("📝 查看手寫發票填寫範例"):
        st.write(f"1. **金額**： 填入 `{sales_amount:,}`")
        st.write(f"2. **營業稅**： 勾選「應稅」，填入 `{tax:,}`")
        st.write(f"3. **總計**： 填入 `{total_amount:,}`")
        st.write(f"4. **總計大寫**： 照抄上方綠色框框文字")

# 清除按鈕 (Streamlit 重新整理頁面即可清空)
if st.button("重新計算"):
    st.rerun()
