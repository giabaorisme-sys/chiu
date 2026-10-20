 
python
    st.markdown("""
    <div class="panel">
        <h3 style="text-align:center">🧩 BẢNG BRAINROT 9×9</h3>
        <p style="text-align:center;color:#b9d7ff">
            Mỗi nhân vật đại diện cho một con số.
            Không được trùng nhân vật trong cùng hàng, cột hoặc vùng 3×3.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 1])

    with left:
        # Board cells use a picture above the selectbox. Streamlit selectboxes
        # display text options; the chosen character image is shown immediately
        # beneath each editable cell.
        with st.form("brainrot_board_form"):
            updated_board = []
            for r in range(9):
                cols = st.columns(9, gap="small")
                row = []
                for c in range(9):
                    with cols[c]:
                        value = puzzle[r][c]
                        if value != 0:
                            path = get_character_file(value)
                            if path and path.exists():
                                st.image(str(path), width=46)
                            else:
                                st.markdown("❓")
                            row.append(value)
                        else:
                            key = cell_key(st.session_state.stage, r, c)
                            # Initialize each selectbox from the saved board.
                            # The key is set before the widget is instantiated.
                            if key not in st.session_state:
                                st.session_state[key] = st.session_state.board[r][c]

                            selected = st.selectbox(
                                f"Ô {r+1}-{c+1}",
                                options=list(range(10)),
                                format_func=get_character_label,
                                key=key,
                                label_visibility="collapsed",
                            )
                            if selected != 0:
                                path = get_character_file(selected)
                                if path and path.exists():
                                    st.image(str(path), width=46)
                                else:
                                    st.caption("Thiếu ảnh")
                            else:
                                st.caption("⬜")
                            row.append(selected)
                updated_board.append(row)

            save = st.form_submit_button("💾 LƯU BÀN CHƠI", use_container_width=True)

        if save:
            st.session_state.board = [row[:] for row in updated_board]
            st.session_state.hint_message = "✅ Đã lưu lựa chọn nhân vật!"
            st.rerun()

    with right:
        st.markdown("### 🌟 Nhân vật")
        for character in CHARACTERS:
            path = ASSETS / character["file"]
            if path.exists():
                st.image(str(path), width=90)
            st.caption(character["name"])

        if st.session_state.get("hint_message"):
            st.info(st.session_state.hint_message)

        st.button("💡 Gợi ý", use_container_width=True, on_click=give_hint)

        if st.button("✓ KIỂM TRA", use_container_width=True):
            # Read the latest selections directly from widget state before checking.
            current_board = [row[:] for row in st.session_state.board]
            for r in range(9):
                for c in range(9):
                    if puzzle[r][c] == 0:
                        current_board[r][c] = st.session_state.get(
                            cell_key(st.session_state.stage, r, c), 0
                        )
            st.session_state.board = current_board

            if any(current_board[r][c] == 0 for r in range(9) for c in range(9)):
                st.warning("Bạn vẫn còn ô trống. Hãy điền đủ các ô trước khi kiểm tra.")
            elif current_board == SOLUTION:
                st.session_state.page = "success"
                st.rerun()
            else:
                st.session_state.mistakes += 1
                st.warning("Chưa đúng hết! Hãy kiểm tra các nhân vật rồi thử lại.")

        st.button("↻ Chơi lại", use_container_width=True, on_click=reset_current_game)


# MÀN HÌNH CHIẾN THẮNG
elif st.session_state.page == "success":
    st.markdown(
        f"""
        <div class="success">
            <div style="font-size:4rem">🏆✨</div>
            <h1 style="color:#ffd44f">HOÀN THÀNH!</h1>
            <h3>Bạn đã chinh phục màn {st.session_state.stage}/5 ({st.session_state.level})</h3>
            <p>Thật tuyệt vời — trí tuệ của bạn đang lên cấp!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Độ khó", st.session_state.level)
    b.metric("Ghi chú đã dùng", f"{st.session_state.notes} lần")
    c.metric("Điểm thưởng", 100 + max(0, 50 - st.session_state.notes * 5))
    st.write("")

    if st.session_state.stage < 5:
        if st.button("➡ TIẾP THEO", use_container_width=True):
            st.session_state.unlocked = max(
                st.session_state.unlocked, st.session_state.stage + 1
            )
            next_stage = st.session_state.stage + 1
            start_stage(next_stage)
    else:
        st.session_state.unlocked = 5
        st.balloons()
        st.success("Bạn đã hoàn thành toàn bộ 5 màn chơi!")

    if st.button("🏠 Về trang chủ", use_container_width=True):
