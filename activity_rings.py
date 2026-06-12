import streamlit as st
import streamlit.components.v1 as components

def render_activity_rings(steps, goal=10000, weekly_data=None):
    # Dış halka (Yeşil)
    first_ring_progress = min(steps / goal, 1.0)
    first_ring_offset = 502.6 - (502.6 * first_ring_progress)
    
    # İç halka (Mavi - 10.000 adım sonrası)
    second_ring_progress = 0.0
    if steps > goal:
        second_ring_progress = min((steps - goal) / goal, 1.0)
    second_ring_offset = 376.9 - (376.9 * second_ring_progress)
    
    total_percentage = int((steps / goal) * 100)
    
    # Sıkışmayı önlemek için dış div yüksekliğini (height) 420px yaptık ve padding'leri rahatlattık
    html_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Segoe UI', sans-serif; background: #111; padding: 20px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.6); width: 280px; height: 380px; margin: auto; box-sizing: border-box;">
        <div style="position: relative; width: 200px; height: 200px;">
            <svg width="200" height="200" viewBox="0 0 200 200" style="transform: rotate(-90deg); position: absolute; top:0; left:0;">
                <circle cx="100" cy="100" r="80" stroke="#222" stroke-width="14" fill="transparent" />
                <circle cx="100" cy="100" r="80" stroke="#00E676" stroke-width="14" fill="transparent"
                        stroke-dasharray="502.6" stroke-dashoffset="{first_ring_offset}" stroke-linecap="round" />
                        
                <circle cx="100" cy="100" r="60" stroke="#151515" stroke-width="12" fill="transparent" />
                <circle cx="100" cy="100" r="60" stroke="#00B0FF" stroke-width="12" fill="transparent"
                        stroke-dasharray="376.9" stroke-dashoffset="{second_ring_offset}" stroke-linecap="round" />
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; width: 100%;">
                <span style="font-size: 32px; font-weight: bold; display: block; color: #00E676;">%{total_percentage}</span>
                <span style="font-size: 11px; color: #888;">Hedef</span>
            </div>
        </div>
        <div style="margin-top: 30px; text-align: center; color: white; width: 100%;">
            <h3 style="margin: 0; font-size: 22px; font-weight: 700; color: #fff;">{steps:,} / {goal:,}</h3>
            <p style="margin: 5px 0 0 0; font-size: 13px; color: #aaa; white-space: nowrap;">Bugünkü Toplam Adımınız</p>
        </div>
    </div>
    """
    # Streamlit iframe yüksekliğini 440 yaparak alttan kırpılmayı tamamen engelliyoruz
    return components.html(html_code, height=440)
