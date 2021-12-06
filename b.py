import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import date, timedelta, datetime

st.set_page_config(
     page_title="Crypto Analyst",
     page_icon="💲",
)
st.title("""
Crypto Analyst

""")
subheader = '<p style="font-family:Courier; color:red; font-size: 20px;">Your Technical Analsyt for Cryto Currencies</p>'
st.markdown(subheader, unsafe_allow_html=True)
CrList=pd.read_csv("docs/crList.csv")
# ticker=CrList["Ticker"][0]
# ticker="BTC-USD"
tickers=CrList["Symbol"]
user_input=st.selectbox("Coin Name",tickers,index=0,help="Please choose the coin you want to analyze.")
ticker=user_input
ticker_names=CrList["Name"]
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        daily_btn = st.button('1D')
    with col2:
        hour_btn = st.button('60m')
    with col3:
        fiveM_btn = st.button('5m')
#Daily Analyze
ticker=user_input
if daily_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1y",interval="1d")
    try:
        ticker_data=yf.download(ticker,period="1y",interval="1d")
        df=pd.DataFrame(ticker_data)
        ticker_date=ticker_data.index
        last_10_days_lastDayExcluded=ticker_date[-10:-1]
        c=df['Close']
        h=df['High']
        l=df['Low']
        last_price=c[-1]
        maxInDate=max(h[ticker_date])
        minInDate=min(l[ticker_date])
        max10=max(h[last_10_days_lastDayExcluded])
        min10=min(l[last_10_days_lastDayExcluded])
        potentialReward=max10-last_price
        risk=last_price-min10
        recommendationList=["New Lows","New High","Buy","Don't Trade"]
        new_low=str(recommendationList[0])
        new_high=str(recommendationList[1])
        buy=str(recommendationList[2])
        dontBuy=str(recommendationList[3])
        @st.cache
        def tradeable():
            if (last_price<min10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_low
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_stopLoss=str("{:.2f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.2f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.2f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.2f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    str_stopLoss=str("{:.2f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except KeyError:
        pass
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.write(newDf)
elif hour_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1mo",interval="60m")
    try:
        df=pd.DataFrame(ticker_data)
        ticker_date=ticker_data.index
        last_10_days_lastDayExcluded=ticker_date[-10:-1]
        c=df['Close']
        h=df['High']
        l=df['Low']
        last_price=c[-1]
        maxInDate=max(h[ticker_date])
        minInDate=min(l[ticker_date])
        max10=max(h[last_10_days_lastDayExcluded])
        min10=min(l[last_10_days_lastDayExcluded])
        potentialReward=max10-last_price
        risk=last_price-min10
        recommendationList=["New Lows","New High","Buy","Don't Trade"]
        new_low=str(recommendationList[0])
        new_high=str(recommendationList[1])
        buy=str(recommendationList[2])
        dontBuy=str(recommendationList[3])
        @st.cache
        def tradeable():
            if (last_price<min10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_low
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_stopLoss=str("{:.2f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.2f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.2f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.2f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    str_stopLoss=str("{:.2f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except KeyError:
        pass
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.write(newDf)
elif fiveM_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ticker_data=yf.download(ticker,period="1d",interval="5m")
    try:
        df=pd.DataFrame(ticker_data)
        ticker_date=ticker_data.index
        last_10_days_lastDayExcluded=ticker_date[-10:-1]
        c=df['Close']
        h=df['High']
        l=df['Low']
        last_price=c[-1]
        maxInDate=max(h[ticker_date])
        minInDate=min(l[ticker_date])
        max10=max(h[last_10_days_lastDayExcluded])
        min10=min(l[last_10_days_lastDayExcluded])
        potentialReward=max10-last_price
        risk=last_price-min10
        recommendationList=["New Lows","New High","Buy","Don't Trade"]
        new_low=str(recommendationList[0])
        new_high=str(recommendationList[1])
        buy=str(recommendationList[2])
        dontBuy=str(recommendationList[3])
        @st.cache
        def tradeable():
            if (last_price<min10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_low
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_stopLoss=str("{:.2f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.2f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.2f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.2f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.2f}".format(min10))
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=str("{:.2f}".format(potentialReward))
                    str_loss_potential=str("{:.2f}".format(risk))
                    str_target_SalePrice=str("{:.2f}".format(max10))
                    str_stopLoss=str("{:.2f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except KeyError:
        pass
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.write(newDf)
st.subheader("Today's Buy List From Top 100 Coins")
#Analyze ALL
analyze_all_btn = st.button('Buy List')
if analyze_all_btn:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="max")
            df=pd.DataFrame(ticker_data)
            # for percent_complete in range(100):
            #     time.sleep(0)
            #     analyze_bar.progress(percent_complete)
            ticker_date=ticker_data.index
            last_10_days_lastDayExcluded=ticker_date[-10:-1]
            c=df['Close']
            h=df['High']
            l=df['Low']
            last_price=c[-1]
            maxInDate=max(h[ticker_date])
            minInDate=min(l[ticker_date])
            max10=max(h[last_10_days_lastDayExcluded])
            min10=min(l[last_10_days_lastDayExcluded])
            potentialReward=max10-last_price
            risk=last_price-min10
            recommendationList=["New Lows","New High","Buy","Don't Trade"]
            new_low=str(recommendationList[0])
            new_high=str(recommendationList[1])
            buy=str(recommendationList[2])
            dontBuy=str(recommendationList[3])
            @st.cache
            def tradeable():
                if (last_price<min10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_low
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_stopLoss=str("{:.2f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.2f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.2f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.2f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.2f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.2f}".format(min10))
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_earn_potential=str("{:.2f}".format(potentialReward))
                        str_loss_potential=str("{:.2f}".format(risk))
                        str_target_SalePrice=str("{:.2f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.2f}".format(min10))
                        str_lastPrice=str("{:.2f} ".format(c[-1]))
                        str_earn_potential=str("{:.2f}".format(potentialReward))
                        str_loss_potential=str("{:.2f}".format(risk))
                        str_target_SalePrice=str("{:.2f}".format(max10))
                        str_stopLoss=str("{:.2f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            # with st.container():
            # with st.spinner(text='Analyzing --    ' + tradeable()[0] ):
            #     time.sleep(0)
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.title(ticker)
                # st.success(newDf[1])
                st.write(newDf)
            else:
                pass
        except KeyError:
            pass
    analzye_finished = '<p style="font-family:Courier; color:red; font-size: 20px;">Finished</p>'
    st.markdown(analzye_finished, unsafe_allow_html=True)
    delete_button = st.button('Clear')

