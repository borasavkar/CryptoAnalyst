import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import date, timedelta, datetime
import time

st.set_page_config(
     page_title="Crypto Analyst",
     page_icon="💲",
)
st.title("""
Crypto Analyst

""")
subheader = '<p style="font-family:Courier; color:red; font-size: 20px;">Your Technical Analsyt for Crypto Currencies</p>'
st.markdown(subheader, unsafe_allow_html=True)
CrList=pd.read_csv("docs/crList.csv")
tickers=CrList["Symbol"]
ticker_names=CrList["Name"]
comma="   -     "
blank_space="      "
display=(tickers+blank_space*50+comma+ticker_names)
display=(ticker_names)
user_input=st.selectbox("Coin Name",tickers,index=0,help="Please choose the coin you want to analyze.",key=tickers)
ticker=user_input
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        daily_btn = st.button('1D',key="1D")
    with col2:
        hour_btn = st.button('60m',key="60m")
    with col3:
        fiveM_btn = st.button('5m',key="5m")
    with col4:
        oneM_btn = st.button('1m',key="1m")
#Daily Analyze
ticker=user_input
if daily_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.subheader("Trade recommendation on daily basis")
    # ticker_data=yf.download(ticker,period="1y",interval="1d")
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
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_stopLoss=str("{:.5f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.5f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.5f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.5f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    str_stopLoss=str("{:.5f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except ValueError:
        st.warning('Not enough data for %s to analyze' % (ticker))
    except MemoryError:
        st.warning("Sorry, your device doesn't have enough memory to continue")
    except KeyError:
        st.warning("Key not found for %s" % (ticker))
    except NameError:
        st.warning(' %s not found to analyze' % (ticker))
    except IndexError:
        st.warning("Index for %s is out of range" % (ticker))
    except GeneratorExit:
        st.warning("Generator's close() method is called for %s" % (ticker))
    except OSError:
        st.warning("System error for %s" % (ticker))
    except RuntimeError:
        st.warning("Runtime error for %s" % (ticker))
    # except:
    except UnboundLocalError:
        st.warning("No value error for %s" % (ticker))
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.table(newDf)
elif hour_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.subheader("Trade recommendation for 1 hour interval")
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
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_stopLoss=str("{:.5f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.5f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.5f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.5f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    str_stopLoss=str("{:.5f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except ValueError:
        st.warning('Not enough data for %s to analyze' % (ticker))
    except MemoryError:
        st.warning("Sorry, your device doesn't have enough memory to continue")
    except KeyError:
        st.warning("Key not found for %s" % (ticker))
    except NameError:
        st.warning(' %s not found to analyze' % (ticker))
    except IndexError:
        st.warning("Index for %s is out of range" % (ticker))
    except GeneratorExit:
        st.warning("Generator's close() method is called for %s" % (ticker))
    except OSError:
        st.warning("System error for %s" % (ticker))
    except RuntimeError:
        st.warning("Runtime error for %s" % (ticker))
    # except:
    except UnboundLocalError:
        st.warning("No value error for %s" % (ticker))
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.table(newDf)
elif fiveM_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.subheader("Trade recommendation for 5 minutes interval")
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
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_stopLoss=str("{:.5f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.5f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.5f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.5f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    str_stopLoss=str("{:.5f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    except ValueError:
        st.warning('Not enough data for %s to analyze' % (ticker))
    except MemoryError:
        st.warning("Sorry, your device doesn't have enough memory to continue")
    except KeyError:
        st.warning("Key not found for %s" % (ticker))
    except NameError:
        st.warning(' %s not found to analyze' % (ticker))
    except IndexError:
        st.warning("Index for %s is out of range" % (ticker))
    except GeneratorExit:
        st.warning("Generator's close() method is called for %s" % (ticker))
    except OSError:
        st.warning("System error for %s" % (ticker))
    except RuntimeError:
        st.warning("Runtime error for %s" % (ticker))
    # except:
    except UnboundLocalError:
        st.warning("No value error for %s" % (ticker))
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.table(newDf)
elif oneM_btn:
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.subheader("Trade recommendation for 1 minute interval")
    ticker_data=yf.download(ticker,period="1d",interval="1m")
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
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=''
                str_target_SalePrice=''
                str_stopLoss=''
                if(minInDate<last_price):
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_stopLoss=str("{:.5f}".format(minInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            elif (last_price>max10):
                str_ticker=str("{}".format(ticker))
                recommendation=new_high
                str_lastPrice=str("{:.5f} ".format(c[-1]))
                str_earn_potential=''
                str_loss_potential=str("{:.5f}".format(last_price-max10))
                str_target_SalePrice=''
                str_stopLoss=str("{:.5f}".format(max10))
                if(maxInDate>last_price):
                    if((maxInDate-last_price)*2>(last_price-max10)):
                        recommendation=buy
                    else:
                        recommendation=dontBuy
                    str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                    str_target_SalePrice=str("{:.5f}".format(maxInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            else:
                if (potentialReward>risk*2):
                    str_ticker=str("{}".format(ticker))
                    recommendation=buy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                else:
                    str_ticker=str("{}".format(ticker))
                    recommendation=dontBuy
                    str_stopLoss=str("{:.5f}".format(min10))
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=str("{:.5f}".format(potentialReward))
                    str_loss_potential=str("{:.5f}".format(risk))
                    str_target_SalePrice=str("{:.5f}".format(max10))
                    str_stopLoss=str("{:.5f}".format(min10))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    except ValueError:
        st.warning('Not enough data for %s to analyze' % (ticker))
    except MemoryError:
        st.warning("Sorry, your device doesn't have enough memory to continue")
    except KeyError:
        st.warning("Key not found for %s" % (ticker))
    except NameError:
        st.warning(' %s not found to analyze' % (ticker))
    except IndexError:
        st.warning("Index for %s is out of range" % (ticker))
    except GeneratorExit:
        st.warning("Generator's close() method is called for %s" % (ticker))
    except OSError:
        st.warning("System error for %s" % (ticker))
    except RuntimeError:
        st.warning("Runtime error for %s" % (ticker))
    # except:
    except UnboundLocalError:
        st.warning("No value error for %s" % (ticker))
    table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sales Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
    newDf=pd.Series(table)
    st.title(ticker)
    if tradeable()[1] == buy or tradeable()[1] == new_high:
        st.success(newDf[1])
    else:
        st.error(newDf[1])
    st.table(newDf)
st.subheader("Analyze Top Crypto Coins Worth Trading")
st.caption("Please press the interval you wish to analyze")
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        daily_btn_all = st.button('1D',key="all_1D")
    with col2:
        hour_btn_all = st.button('60m',key="all_60m")
    with col3:
        fiveM_btn_all = st.button('5m',key="all_5m")
    with col4:
        oneM_btn_all = st.button('1m',key="all_1m")
#Analyze ALL 1D
if daily_btn_all:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1y",interval="1d")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#Analyze ALL 60m
elif hour_btn_all:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1mo",interval="60m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#Analyze ALL 5m
elif fiveM_btn_all:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1d",interval="5m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#Analyze ALL 1m
elif oneM_btn_all:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="60m",interval="1m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*2):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
            
    analzye_finished = '<p style="font-family:Courier; color:red; font-size: 20px;">Finished!</p>'
    st.markdown(analzye_finished, unsafe_allow_html=True)
    delete_button = st.button('Clear',key="clear")
st.subheader("Analyze Coins That Gives Strong Buy Signal")
st.caption("Please press the interval you wish to analyze")
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        daily_btn_strong = st.button('1D',key="strong_1D")
    with col2:
        hour_btn_strong = st.button('60m',key="strong_60m")
    with col3:
        fiveM_btn_strong = st.button('5m',key="strong_5m")
    with col4:
        oneM_btn_strong = st.button('1m',key="strong_1m")
#strong ALL 1D
if daily_btn_strong:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1y",interval="1d")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*4):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#strong ALL 60m
elif hour_btn_strong:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1mo",interval="60m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*4):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#strong ALL 5m
elif fiveM_btn_strong:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="1d",interval="5m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*4):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
#strongALL 1m
elif oneM_btn_strong:
    ticker=user_input
    st.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    analyze_bar = st.progress(0)
    for i in tickers:
        try:
            ticker = i
            ticker_data=yf.download(ticker,period="60m",interval="1m")
            df=pd.DataFrame(ticker_data)
            for percent_complete in range(100):
                time.sleep(0.0001)
                analyze_bar.progress(percent_complete+1)
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
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=''
                    str_target_SalePrice=''
                    str_stopLoss=''
                    if(minInDate<last_price):
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_stopLoss=str("{:.5f}".format(minInDate))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                elif (last_price>max10):
                    str_ticker=str("{}".format(ticker))
                    recommendation=new_high
                    str_lastPrice=str("{:.5f} ".format(c[-1]))
                    str_earn_potential=''
                    str_loss_potential=str("{:.5f}".format(last_price-max10))
                    str_target_SalePrice=''
                    str_stopLoss=str("{:.5f}".format(max10))
                    if(maxInDate>last_price):
                        if((maxInDate-last_price)*2>(last_price-max10)):
                            recommendation=buy
                        else:
                            recommendation=dontBuy
                        str_earn_potential=str("{:.5f}".format(maxInDate-last_price))
                        str_target_SalePrice=str("{:.5f}".format(maxInDate))
                    return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
                else:
                    if (potentialReward>risk*4):
                        str_ticker=str("{}".format(ticker))
                        recommendation=buy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   
                    else:
                        str_ticker=str("{}".format(ticker))
                        recommendation=dontBuy
                        str_stopLoss=str("{:.5f}".format(min10))
                        str_lastPrice=str("{:.5f} ".format(c[-1]))
                        str_earn_potential=str("{:.5f}".format(potentialReward))
                        str_loss_potential=str("{:.5f}".format(risk))
                        str_target_SalePrice=str("{:.5f}".format(max10))
                        str_stopLoss=str("{:.5f}".format(min10))
                        return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            if tradeable()[1] == buy or tradeable()[1] == new_high:
                table={'Name:':tradeable()[0],'Trade Recommendation:':tradeable()[1],'Last Price:':tradeable()[2],'Earn Potential:':tradeable()[3],'Loss Potential:':tradeable()[4],'Target Sale Price:':tradeable()[5],'Stop-Loss:':tradeable()[6]}
                newDf=pd.Series(table)
                st.success(ticker)
                st.table(newDf)
            else:
                pass
        except ValueError:
            st.warning('Not enough data for %s to analyze' % (i))
        except MemoryError:
            st.warning("Sorry, your device doesn't have enough memory to continue")
        except KeyError:
            st.warning("Key not found for %s" % (i))
        except NameError:
            st.warning(' %s not found to analyze' % (i))
        except IndexError:
            st.warning("Index for %s is out of range" % (i))
        except GeneratorExit:
            st.warning("Generator's close() method is called for %s" % (i))
        except OSError:
            st.warning("System error for %s" % (i))
        except RuntimeError:
            st.warning("Runtime error for %s" % (i))
        # except:
        except UnboundLocalError:
            st.warning("No value error for %s" % (i))
            
    analzye_finished = '<p style="font-family:Courier; color:red; font-size: 20px;">Finished!</p>'
    st.markdown(analzye_finished, unsafe_allow_html=True)
    delete_button = st.button('Clear',key="clear")