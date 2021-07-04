import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar
import matplotlib.dates as mdates

class Econ():

    def __init__(self):

        self.country_dict = {
            "中國":"China",
            "台灣":"TW",
            "臺灣":"TW",
            "美國":"USA",
            "全球":"World",
            "日本":"JP",
            "泰國":"Thailand",
            "俄羅斯":"Russia",
            "巴西":"Brazil",
            "印度":"India"
        }
        ## format: index_group = [df_Stock_Index, df_Industrial_Index, df_MA, df_Interest_Rate, df_PMI, df_GDP]
        self.asset_dict = {
            "股票":[1,1,1,1,1,1],
            "投資型債券":[-1,-1,-1,-1,-1,-1],
            "高收益債券":[1,1,1,1,1,1],
            "定存":[-1,1,0,1,-1,1],
            "房地產":[1,1,1,-1,1,1],
        }
        self.index_list = ["Stock_Index", "Industrial_Index", "MA", "Interest_Rate", "PMI", "GDP"]
        self.fund_pool = self.read_fund_pool()
        self.econ_df = {}
        self.econ_check = {}
        self.read_all_index()
        self.recommend_fund = []
        self.profit = self.read_profit()

    def read_all_index(self):

        countries = list(self.country_dict.values())
        country_set = set(countries)
        country_list = list(country_set)

        for country in country_list:
            country_index, country_check = self.read_index(country)
            self.econ_df[country] = country_index.copy()
            self.econ_check[country] = country_check.copy()        

    def read_index(self, country):
    
        file_d = "database/Economic_index/" + country + "_index/"
        index_group = []
        index_check = []
        try:
            df_Stock_Index      = pd.read_csv(file_d+country+"_Stock_Index.csv")
            index_group.append(df_Stock_Index)
            index_check.append(True)
        except:
            df_Stock_Index      = None
            index_group.append(df_Stock_Index)
            index_check.append(False)
        try:
            df_Industrial_Index   = pd.read_csv(file_d+country+"_Industrial_Index.csv")
            index_group.append(df_Industrial_Index)
            index_check.append(True)
        except:
            df_Industrial_Index   = None
            index_group.append(df_Industrial_Index)
            index_check.append(False)
        try:
            df_MA               = pd.read_csv(file_d+country+"_MA.csv")
            index_group.append(df_MA)
            index_check.append(True)
        except:
            df_MA               = None
            index_group.append(df_MA)
            index_check.append(False)
        try:
            df_Interest_Rate    = pd.read_csv(file_d+country+"_Interest_Rate.csv")
            index_group.append(df_Interest_Rate)
            index_check.append(True)
        except:
            df_Interest_Rate    = None
            index_group.append(df_Interest_Rate)
            index_check.append(False)
        try:
            df_PMI              = pd.read_csv(file_d+country+"_PMI.csv")
            index_group.append(df_PMI)
            index_check.append(True)
        except:
            df_PMI              = None
            index_group.append(df_PMI)
            index_check.append(False)
        try:
            df_GDP              = pd.read_csv(file_d+country+"_GDP.csv")
            index_group.append(df_GDP)
            index_check.append(True)
        except:
            df_GDP              = None
            index_group.append(df_GDP)
            index_check.append(False)
        
        # df_Interest_Rate    = pd.read_csv(file_d+country+"_Interest_Rate.csv")
        # df_Stock_Index      = pd.read_csv(file_d+country+"_Stock_Index.csv")
        # df_MA               = pd.read_csv(file_d+country+"_MA.csv")
        # df_PMI              = pd.read_csv(file_d+country+"_PMI.csv")
        # df_GDP              = pd.read_csv(file_d+country+"_GDP.csv")

        # index_group = [df_Stock_Index, df_Industrial_Index, df_MA, df_Interest_Rate, df_PMI, df_GDP]

        return index_group, index_check

    def data_preprocess(self, df):
        
        ## adjust date format
        ## ex: "2021-5-4" -> "2021-05-04"
        df = df.dropna()
        # print(df)
        
        for i in range(len(df)):
            old_date = df.iat[i, 0]
            # print(old_date)
            if "/" in old_date:
                old_date = old_date.split("/")
            elif "-" in old_date:
                old_date = old_date.split("-")
            
            new_date = datetime.date(int(old_date[0]),int(old_date[1]),int(old_date[2]))
            df.iat[i, 0] = new_date
            
        ## adjust value
        if "value" in df.columns:
            df["value"] = pd.to_numeric(df["value"], errors='coerce')
            # print(df.iloc[:50,:])
            df = df.dropna()
            
            ## calculate growth rate
            value = df["value"]
            value = value.to_numpy()
            delta = [(value[i+1]-value[i])/value[i] for i in range(len(value)-1)]
            delta.insert(0, 0)
            df.insert(2, column="growth", value=delta)
            
        elif "rate" in df.columns:
            value = df["rate"]
            value = value.to_numpy()
            delta = [(value[i+1]-value[i]) for i in range(len(value)-1)]
            delta.insert(0, 0)
            df.insert(2, column="diff", value=delta)
            pass

        return df

    def read_fund_pool(self):
        
        ## format: Index(['名稱', '風險', '類型', '地區', '產業'], dtype='object')
        file_name = "database/fund_pool.csv"
        df = pd.read_csv(file_name)
        df = df.drop("比例", axis=1)
        # df = df.dropna()
        # print(df)
        return df

    def read_profit(self):

        profit_pool = []
        PATH = "database/profit/"
        for i in range(len(self.fund_pool)):
            item = self.fund_pool.loc[i,"名稱"]
            data = PATH+item+".csv"
            df = pd.read_csv(data)
            profit_pool.append(df)

        return profit_pool

    def plot_index(self, df):
        
        fig = plt.figure(figsize=(12,8))
        
        idx = df.drop(df.columns[0], axis=1)
        idx = idx.to_numpy()
        date = df.drop(df.columns[-1], axis=1)
        date = date[df.columns[0]].values.tolist()
        print(date[0])

        x = [datetime.strptime(d, '%Y/%m/%d').date() for d in date]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100)) #座標軸刻度1天

        # plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        # plt.gca().yaxis.set_major_locator(mdates.MinuteLocator(interval=10)) #座標軸刻

        plt.subplots_adjust(bottom=0.25) 
        plt.plot(x,idx)
        plt.xticks(rotation=90)
        # plt.xticks(x,date)
        plt.legend()
        plt.show()

    def Stock_Index_eval(self, df, period):

        df = self.data_preprocess(df)
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        # if "value" in df.columns:
        #     value = df["value"]
        #     if value[target_date] < value[len(value)-1]:
        #         judge = 1
        #     else:
        #         judge = 0
        # elif "rate" in df.columns:
        #     diff = df["diff"]
        #     if diff[len(diff)-1] > 0:
        #         judge = 1
        #     else:
        #         judge = 0
        
        if "value" in df.columns:
            value = df["value"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0
        elif "rate" in df.columns:
            value = df["diff"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0

        return judge

    def Industrial_Index_eval(self, df, period):

        df = self.data_preprocess(df)
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        # if "value" in df.columns:
        #     value = df["value"]
        #     if value[target_date] < value[len(value)-1]:
        #         judge = 1
        #     else:
        #         judge = 0
        # elif "rate" in df.columns:
        #     diff = df["diff"]
        #     if diff[len(diff)-1] > 0:
        #         judge = 1
        #     else:
        #         judge = 0

        if "value" in df.columns:
            value = df["value"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0
        elif "rate" in df.columns:
            value = df["diff"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0

        return judge

        return judge

    def MA_eval(self, df, period):

        df = self.data_preprocess(df)
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        # if "value" in df.columns:
        #     value = df["value"]
        #     if value[target_date] < value[len(value)-1]:
        #         judge = 1
        #     else:
        #         judge = 0
        # elif "rate" in df.columns:
        #     diff = df["diff"]
        #     if diff[len(diff)-1] > 0:
        #         judge = 1
        #     else:
        #         judge = 0

        if "value" in df.columns:
            value = df["value"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0
        elif "rate" in df.columns:
            value = df["diff"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0

        return judge

    def Interest_Rate_eval(self, df, period):
        
        df = self.data_preprocess(df)

        value = df[df.columns[1]]
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        # if value[target_date] < value[len(value)-1]:
        #     judge = 1
        # else:
        #     judge = 0

        pos, neg = 0, 0
        for i in range(target_date, len(value)):
            if value[i] >= 0:
                pos += 1
            else:
                neg += 1

        if pos >= neg:
            judge = 1
        else:
            judge = 0


        return judge

    def PMI_eval(self, df, period):

        df = self.data_preprocess(df)

        value = df[df.columns[1]]
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        pos, neg = 0, 0
        for i in range(target_date, len(value)):
            if value[i] >= 50:
                pos += 1
            else:
                neg += 1

        if pos >= neg:
            judge = 1
        else:
            judge = 0

        return judge

    def GDP_eval(self, df, period):
        
        df = self.data_preprocess(df)
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        # if "value" in df.columns:
        #     value = df["value"]
        #     if value[target_date] < value[len(value)-1]:
        #         judge = 1
        #     else:
        #         judge = 0
        # elif "rate" in df.columns:
        #     diff = df["diff"]
        #     if diff[len(diff)-1] > 0:
        #         judge = 1
        #     else:
        #         judge = 0

        if "value" in df.columns:
            value = df["value"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0
        elif "rate" in df.columns:
            value = df["diff"]
            pos, neg = 0, 0
            for i in range(target_date, len(value)):
                if value[i] >= 0:
                    pos += 1
                else:
                    neg += 1

            if pos >= neg:
                judge = 1
            else:
                judge = 0

        return judge

    def growth_eval(self, df, period):
        
        df = self.data_preprocess(df)

        value = df[df.columns[1]]
        date = df[df.columns[0]]

        target_date = 0
        for idx, d in enumerate(date):
            if d > period:
                target_date = idx
                break
        
        ## evaluate index
        ## TODO: 有其他更好的判斷準則嗎?
        if value[target_date] < value[len(value)-1]:
            judge = 1
        else:
            judge = 0

        return judge

    def evaluation(self, df_list, df_check, period):
        
        ## TODO: 可以調整各指標之評斷標準
        eval_list = []
        for i in range(len(df_list)):
            if df_check[i] == True:
                if i == 0:
                    # result = growth_eval(target_index[i], period)
                    result = self.Stock_Index_eval(df_list[i], period)
                elif i == 1:
                    # result = growth_eval(target_index[i], period)
                    result = self.Industrial_Index_eval(df_list[i], period)
                elif i == 2:
                    # result = growth_eval(target_index[i], period)
                    result = self.MA_eval(df_list[i], period)
                elif i == 3:
                    # result = growth_eval(target_index[i], period)
                    result = self.Interest_Rate_eval(df_list[i], period)
                elif i == 4:
                    # result = growth_eval(target_index[i], period)
                    result = self.PMI_eval(df_list[i], period)
                elif i == 5:
                    # result = growth_eval(target_index[i], period)
                    result = self.GDP_eval(df_list[i], period)
                # print("result: ", self.index_list[i], result)
                eval_list.append(result)
            else:
                # print("result: ", self.index_list[i], None)
                eval_list.append(np.nan)
        
        return eval_list

    def fund_evaluation(self):

        #####################################
        ## information from user's reply
        ## TODO: 還有其他可以參考的資訊嗎?
        risk_level = 4



        #####################################
        
        ## fund testing
        fund_score = np.zeros(len(self.fund_pool))
        for target_fund in range(len(self.fund_pool)):
        # for target_fund in range(47, 48):
            
            # print(target_fund, self.fund_pool.iloc[target_fund,0], self.fund_pool.iloc[target_fund,3])
            # target = df.iloc[target_fund,:]
            try:
                target_index, target_check = self.read_index(self.country_dict[self.fund_pool.iloc[target_fund,3]])
            except:
                # print("="*20)
                continue
            
            ## choosing period for evaluation
            today = datetime.date.today()
            ## 欲觀察的總經指數期長(單位:年)
            ## TODO: 自行挑整看看?(不要太長或太短)
            t_delta = 3         
            t_day = today.replace(year=today.year - t_delta)
            # time_del = datetime.timedelta(days=3) 
            # t_day = datetime.date.today() - time_del
            
            
            ## evaluate index
            # 目前的評估方式:
            # 如果是實際數據，則計算成長率( = (v1-v0)/v0 ) -> 記錄在"growth"
            # 若目前數值(value) > 歷史數值 -> 看好
            # 如果是成長率，則計算成長百分點 ( = r1-r0 )   -> 記錄在"diff"
            # 若近期成長率為正 -> 看好
            ## TODO: 若想試試其他的判斷方式，可以直接到該function裡修改
            
            eval_list = self.evaluation(target_index, target_check, t_day)
            # print("評估結果", eval_list)

            ## final result
            asset = self.fund_pool.iloc[target_fund,2]
            if "多重資產" in asset:
                asset_list = ["多重資產"]
                ## 暫時先不處理多重資產，等mentor回覆
            else:
                asset_list = asset.split("/")
            # print("資產類型", asset_list)
            final_eval = []
            for asset_idx in asset_list:
                asset_judge = self.asset_dict.get(asset_idx)
                if asset_judge != None:
                    eval_list_temp = np.array(eval_list)
                    eval_list_temp = eval_list_temp - 0.5
                    asset_list_temp = np.array(asset_judge)
                    result_list = eval_list_temp * asset_list_temp
                    result_list = result_list + 0.5
                    final_judge = np.nanmean(result_list)
                    final_eval.append(final_judge)
                    # print("資產類型", asset_idx)
                    # print("指數升/降", np.array(eval_list))
                    # print("指數/資產相關性", asset_list_temp)
                    # print("評估結果(看好/看壞)", result_list, final_judge)
            final_result = np.nanmean(final_eval)
            # print("最終結果", final_result)
            # print("="*20)
            if np.isnan(final_result) == False:
                fund_score[target_fund] = final_result
        
        # print('!'*20)
        # print(fund_score)
        recommend_list = []
        for fs in range(len(fund_score)):
            if fund_score[fs] >= 0.5:
                recommend_list.append(fs)

        self.recommend_fund = recommend_list.copy()

        return recommend_list
        ## end of fund testing
        ######################################

    def fund_filter(self, risk):

        final_list = []
        if len(self.recommend_fund) > 0:
            for i in self.recommend_fund:
                fund_risk = self.fund_pool.loc[i, "風險"]
                fund_risk = int(fund_risk[-1])
                if risk >= fund_risk:
                    final_list.append(i)

        return final_list

    def get_short_recommend_list(self, recommend_list):

        df = self.fund_pool.iloc[recommend_list]
        df = df.sort_values(by = '一年績效', ascending=False)
        # print(df.index.to_list())
        return df.index.to_list()
        pass

    def gen_recommend_text(self, recommend_list, risk_result,short):

        fund_text = ""
        if len(recommend_list) > 0:
            for idx, fund in enumerate(recommend_list):
                
                fund_text += self.fund_pool.loc[fund,"風險"]
                fund_text += "     "
                fund_text += self.fund_pool.loc[fund,"名稱"]
                if self.fund_pool.loc[fund,"推薦"] == 1:
                    fund_text += "     "
                    fund_text += "👑"
                fund_text += "\n"
                if short:
                    if idx > 1:
                        break
        else:
            match_list = []
            # print(self.fund_pool.tail())
            print("RRR", len(self.fund_pool))
            for idx in range(len(self.fund_pool)):
                # print(idx, self.fund_pool.loc[idx,"風險"][2:])
                risk = int(self.fund_pool.loc[idx,"風險"][2:])
                # print("ii", risk_result)
                # print("RR", risk)
                # print("MM", match_list)
                # print(type(risk), type(risk_result))
                if risk <= risk_result:
                    match_list.append(idx)
            print(match_list)
            match_list = self.get_short_recommend_list(match_list)
            print(match_list)
            for idx, fund in enumerate(match_list):
                fund_text += self.fund_pool.loc[fund,"風險"]
                fund_text += "     "
                fund_text += self.fund_pool.loc[fund,"名稱"]
                if self.fund_pool.loc[fund,"推薦"] == 1:
                    fund_text += "     "
                    fund_text += "👑"
                fund_text += "\n"
                if short:
                    if idx > 2:
                        break

        # print("HERE")
        if len(recommend_list) == 0:
            top = "📝以下是NomuraBot找到符合你風險承受度的基金\n基金名稱後方有顯示👑圖示的話，代表是目前野村投信主推的基金\n"
            fund_text = top + fund_text
        else:
            top = "📝以下是NomuraBot幫你精挑細選的的基金\n基金名稱後方有顯示👑圖示的話，代表是目前野村投信主推的基金\n"
            fund_text = top + fund_text
            pass

        return fund_text

    def get_fund_info(self, fund_text):

        target_fund = None
        for i in range(len(self.fund_pool)):
            if self.fund_pool.loc[i,"名稱"] == fund_text:
                target_fund = self.fund_pool.loc[i,:].to_list()
                target_fund.append(i)
                break

        return target_fund

    def cal_profit(self, name, period, initial, invest):

        # return (100, 50)
        print(name, period, initial, invest)
        target_fund = None
        for i in range(len(self.fund_pool)):
            if self.fund_pool.loc[i,"名稱"] == name:
                target_fund = i
                break

        if target_fund == None:
            return None
        else:
            df = self.profit[target_fund].copy()
            for i in range(len(df)):
                old_date = df.iat[i, 0]
                # print(old_date)
                if "/" in old_date:
                    old_date = old_date.split("/")
                elif "-" in old_date:
                    old_date = old_date.split("-")
                
                new_date = datetime.date(int(old_date[0]),int(old_date[1]),int(old_date[2]))
                df.iat[i, 0] = new_date

            today = datetime.date.today()
            t_delta = period   
            t_day = today.replace(year=today.year - t_delta)

            date = df[df.columns[0]]
            value = df[df.columns[1]]
            target_date = 0
            # print(date)
            # print("A")
            for idx, d in enumerate(date):
                if d > t_day:
                    target_date = idx
                    break
            # print("B")
            
            # print(df.iloc[target_date:,1])
            value_period = df.iloc[target_date:,1].to_list()
            max_profit = max(value_period)
            min_profit = min(value_period)
            max_result = 100*(max_profit-value_period[0])
            min_result = 100*(min_profit-value_period[0])
            # print(max_profit-value_period[0], type(max_profit-value_period[0]))
            return (float('{:.2f}'.format(max_result)), float('{:.2f}'.format(min_result)))
            # return (max_profit-value_period[0],min_profit-value_period[0])


        # if target_fund == None:
        #     return None
        # else:
        #     # print(target_fund)
        #     df = self.profit[target_fund]
        #     for i in range(len(df)):
        #         old_date = df.iat[i, 0]
        #         # print(old_date)
        #         if "/" in old_date:
        #             old_date = old_date.split("/")
        #         elif "-" in old_date:
        #             old_date = old_date.split("-")
                
        #         new_date = datetime.date(int(old_date[0]),int(old_date[1]),int(old_date[2]))
        #         df.iat[i, 0] = new_date

        #     if invest == None:
        #         profit_list = []
        #         for i in range(len(df)):
        #             start_date = df.iat[i, 0]
        #             start_value = df.iat[i, 1]
        #             if calendar.monthrange(start_date.year + period, start_date.month)[1] < start_date.day:
        #                 due_date = start_date.replace(day=calendar.monthrange(start_date.year + period, start_date.month)[1])
        #                 due_date = due_date.replace(year=start_date.year + period)
        #             else:
        #                 due_date = start_date.replace(year=start_date.year + period)
        #             print(due_date)
        #             end_date = None
        #             for j in range(len(df)):
        #                 if df.iat[j, 0] > due_date:
        #                     end_date = df.iat[j, 0]
        #                     end_value = df.iat[j, 1]
        #                     break
        #             if end_date == None:
        #                 break
        #             else:
        #                 # value = end_value - start_value
        #                 profit_sum = initial*(1+end_value-start_value)
        #                 profit_list.append(profit_sum)

        #         max_profit = max(profit_list)
        #         min_profit = min(profit_list)
        #         return (max_profit, min_profit)
        #     else:
        #         profit_list = []
        #         for i in range(len(df)):
        #             start_date = df.iat[i, 0]
        #             start_value = df.iat[i, 1]
        #             due_date = start_date.replace(year=start_date.year + period)
        #             end_date = None
        #             for j in range(len(df)):
        #                 if df.iat[j, 0] > due_date:
        #                     end_date = df.iat[j, 0]
        #                     end_value = df.iat[j, 1]
        #                     break
        #             if end_date == None:
        #                 break
        #             else:
        #                 # value = end_value - start_value
        #                 profit_sum = initial*(1+end_value-start_value)
        #                 profit_list.append(profit_sum)

        #         max_profit = max(profit_list)
        #         min_profit = min(profit_list)
        #         return (max_profit, min_profit)



if __name__ == '__main__':

    # recommend_fund =  fund_evaluation()
    # print("recommend: ", recommend_fund)
    
    # countries = list(Econ_handler.country_dict.values())
    # country_set = set(countries)
    # country_list = list(country_set)
    # print(country_list)
    
    Econ_handler = Econ()
    recommend_list = Econ_handler.fund_evaluation()
    print("r", recommend_list)

    A = Econ_handler.cal_profit("野村精選貨幣市場基金", 9, 50, None)
    print(A)
    # open('database/market_graph/全球.PNG', 'rb')

    # print(Econ_handler.fund_pool)
    # print(Econ_handler.fund_pool.loc[0,"推薦"])
    # print(Econ_handler.fund_pool.loc[20,"推薦"])
    # Econ_handler.get_short_recommend_list(recommend_list)
    # print(Econ_handler.fund_pool.loc[20,:].to_list())

    

