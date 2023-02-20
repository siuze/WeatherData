import pandas as pd
import pymysql 
import plotly.graph_objects as go
import os


    
def draw_chart_week():
	con = pymysql.connect(host = os.environ["SQL_HOST"],port=int(os.environ["SQL_PORT"]),user=os.environ["SQL_USER"],password=os.environ["SQL_PASSWORD"],db=os.environ["SQL_DB"])
	data_sql=pd.read_sql("SELECT Time,Temp,Hum,Press,Rain from zcs where Time >= DATE_SUB(NOW(),INTERVAL 7 DAY) ORDER BY Time ",con)
	# plot = px.area(data_frame=data_sql,x='Time',y='Temp',orientation='h')
	Temp_avg=data_sql['Temp'].mean()
	Temp_min=data_sql['Temp'].min()
	Temp_max=data_sql['Temp'].max()
	Temp_min_fix=Temp_min-(Temp_max-Temp_min)*0.4
	if Temp_min_fix<0:
		Temp_min_fix=0
	Hum_avg=data_sql['Hum'].mean()
	# fig = make_subplots(specs=[[{"secondary_y": True}]])
	# fig = go.Figure()
	layout = go.Layout(
		# paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)'
		, title="近一周气象观测数据"
	)

	fig = go.Figure(layout=layout)
	bga=data_sql[(data_sql['Time'].dt.hour == 20) & (data_sql['Time'].dt.minute == 0) ]
	if pd.to_datetime(data_sql.iloc[0]['Time']).strftime("%Y-%m-%d") != pd.to_datetime(bga.iloc[0]['Time']).strftime("%Y-%m-%d"):
		bga = pd.concat([data_sql[0:1],bga])	
	a_list=[]
	for i in range(bga.shape[0]):
		a_list.append(int((i)%2==0))
	fig.add_trace(go.Histogram(
		x=bga['Time'],y=a_list,
		#  x=['2023-02-07 20:00','2023-02-08 20:00','2023-02-09 20:00','2023-02-10 20:00','2023-02-11 20:00','2023-02-12 20:00',],y=[30,0,30,0,30,0],
		histfunc='sum',
		xbins={"start":'2023-01-01 20:00',"size" : 1000*60*60*24},
		yaxis="y",
		#  marker_color="#b2bbbe",
		marker=dict(
				color='rgba(178, 187, 190, 0.2)',
		
			),
		showlegend=False,
		hoverinfo='skip',
		name="背景",
	),)
	fig.add_trace( go.Scatter(
			x=data_sql['Time'],y=data_sql['Temp'],
		mode='lines',
		name="气温",
		#  hoverinfo='name',
		line={'shape': 'spline', 'smoothing': 1.3, 'width' : 1 , 'color' : '#ed5a65'},
		#  fill='tonexty',
		yaxis="y5",
	hovertemplate='%{y} ℃',

		# marker_colorscale=plotly.colors.sequential.Viridis
		
					))

	fig.add_trace( go.Scatter(
			x=data_sql['Time'],y=data_sql['Hum'],
		mode='lines',
		#  fill='tonexty',
		name="湿度",
		#  hoverinfo='name',
	hovertemplate='%{y} %RH',
		line={'shape': 'spline', 'smoothing': 1.3, 'width' : 1, 'color' : '#c6e6e8' },
		yaxis="y3",
		
					),)
	fig.add_trace( go.Scatter(
			x=data_sql['Time'],y=data_sql['Press'],
		mode='lines',
		#  fill='tonexty',
		name="气压",
	hovertemplate='%{y} hPa',
		#  hoverinfo='name',
		line={'shape': 'spline', 'smoothing': 1.3, 'width' : 1, "color":"#e2e1e4"},
		yaxis="y2",
		
					),)

	fig.add_trace(go.Histogram(
		x=data_sql['Time'],y=data_sql['Rain'],
		histfunc='sum',
		autobinx=False,
		#   nbinsy = 10,
		#   nbinsx = 10,
		xbins={"size" : 1000*60*60},
	hovertemplate='%{y} mm/h',
		yaxis="y4",
		marker_color="#83cbac",
		# marker=dict(color="#45b787",),
		name="降水",
		#  xbins=dict(
		#                              start='2018-01-01',
		#                              end='2019-12-30',
		#                              size='M2'
		#                          )

	),)


	fig.add_trace( go.Scatter(
			x=data_sql['Time'],y=data_sql['Temp'],
		mode='lines',
		name="气温",
		#  hoverinfo='name',
		line={'shape': 'spline', 'smoothing': 1.3, 'width' : 0 , 'color' : '#ed5a65'},
		#  fill='tonexty',
		yaxis="y6",showlegend=False,
		hoverinfo='skip'
					))
	# fig.add_hline(y=15, line_width=3, line_dash="dash", line_color='#8fb2c9')

	fig.add_trace(go.Scatter(
		x=[data_sql.iat[0, 0],data_sql.iat[-1, 0]],y=[Temp_avg,Temp_avg],
		mode='lines',
		name="均温",
		
		hoverinfo='skip',
		yaxis="y6",showlegend=False,
	line={'shape': 'spline', 'dash':'dash','smoothing': 1.3, 'width' : .5, 'color' : '#eba0b3'},
		#  visible='legendonly'
	))
	fig.add_trace(go.Scatter(
		x=[data_sql.iat[0, 0],data_sql.iat[-1, 0]],y=[Hum_avg,Hum_avg],
		mode='lines',
		hoverinfo='skip',
		name="均湿",
		#  hoverinfo='value',
		line={'shape': 'spline','dash':'dash', 'smoothing': 1.3, 'width' : .5, 'color' : '#8fb2c9'},
		showlegend=False,
		yaxis="y3",
		#  visible='legendonly'
	),)

	fig.update_layout(
		xaxis=dict(
		linecolor="#b2bbbe",
			# domain=[0, 0.94],
			gridcolor ="#b2bbbe",
			mirror=True
		),
		yaxis4=dict(
		showgrid=False,
		showticklabels=False,
				range=[0,30],
			dtick=.2,
				
			title="",
			titlefont=dict(
				color="#45b787"
			),
			tickfont=dict(
				color="#45b787",size=10
			),
			anchor="free",
			overlaying="y",
			side="right",
			position=0.99
		
		),
		yaxis=dict(
		# overlaying="y",
		range=[0,1],
		showgrid=False,
		showticklabels = False,
		# showtick=False,
		linecolor="#e2e1e4",
			title="",
			titlefont=dict(
				color="#ed5a65",
				size=10
			),
			tickfont=dict(
				color="#ed5a65",
				size=10
				
			),
			gridcolor ="#e2e1e4",
			dtick=1,
			title_standoff  =  0 ,
			
		),
		yaxis6=dict(
		overlaying="y",
		range=[Temp_min_fix,Temp_max],
		showgrid=True,
		# showline=False,
		linecolor="#e2e1e4",
			title="气温/℃",
			titlefont=dict(
				color="#ed5a65",
				size=10
			),
			tickfont=dict(
				color="#ed5a65",
				size=10
				
			),
			gridcolor ="#e2e1e4",
			dtick=1,
			title_standoff  =  0 ,
			
		),
		yaxis5=dict(
		overlaying="y",
		range=[Temp_min_fix,Temp_max],
		showgrid=False,
		showticklabels = False,
		# showtick=False,
		linecolor="#e2e1e4",
			title="",
			titlefont=dict(
				color="#ed5a65",
				size=10
			),
			tickfont=dict(
				color="#ed5a65",
				size=10
				
			),
			gridcolor ="#e2e1e4",
			dtick=1,
			title_standoff  =  0 ,
			
		),
		yaxis2=dict(
		showticklabels=False,
		showgrid=False,
			title="",
			dtick=0.4,
		
			tickfont=dict(
				color="#e2e1e4",size=10
			),
			anchor="free",
			overlaying="y",
			side="right",
			position=0.99,
		),
		yaxis3=dict(
		showgrid=False,
			title="湿度/%RH",
			titlefont=dict(
				color="#5cb3cc",
				size=10
				
			),
			dtick=4,
			tickfont=dict(
				color="#5cb3cc",
				size=10
			),
			title_standoff  =  1 ,
			anchor="y",
			overlaying="y",
			side="right",
			# position=0.95,
		linecolor="#e2e1e4",
			
			
		),
	)

	# fig['layout']['yaxis2']['autorange'] = "reversed"
	# fig['layout']['yaxis3']['autorange'] = "reversed"
	fig.update_layout(hovermode="x unified",hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)'),)
	# fig.update_xaxes(showspikes=True)  # <-- add this line
	# fig.update_yaxes(showspikes=True)  # <-- add this line

	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
	),
	margin=dict(l=50, r=50, t=100, b=0),
	)
	# fig.update_yaxes(separatethousands=False)
	fig.update_xaxes(ticks= "outside",
					ticklabelmode= "period", 
					tickcolor= "black", 
					ticklen=10, 
					minor=dict(
						ticklen=4,  
						dtick=60*60*1000, 
						griddash='dot', 
						gridcolor='#e2e1e4'),
						hoverformat='%Y年%m月%d日 %H:%M'
					)
	fig.write_image("chart.jpg", height=450, width=800, scale=10)
	fig.update_xaxes(
		rangeslider_visible=True,
			rangeselector=dict(
			buttons=list([
				dict(count=6, label="6小时", step="hour", stepmode="backward"),
				dict(count=12, label="12小时", step="hour", stepmode="backward"),
				dict(count=24, label="24小时", step="hour", stepmode="backward"),
				dict(count=48, label="48小时", step="hour", stepmode="backward"),
				dict(count=1, label="当日", step="day", stepmode="todate"),
				dict(label="近一周",step="all")
			])
		),
		tickformatstops = [
			dict(dtickrange=[60*1000, 3*60*60*1000], value="%H:%M \n %m月%d日"),
			dict(dtickrange=[3*60*60*1000, 23*60*60*1000], value="%H时 \n %m月%d日"),
			dict(dtickrange=[23*60*60*1000, "M12"], value="%m月%d日"),
			# dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
			# dict(dtickrange=["M1", "M12"], value="%b '%y M"),
			# dict(dtickrange=["M12", None], value="%Y Y")
		]
	)
	# fig.show()
	fig.write_html(
					'chart.html',
					full_html=True,
					include_plotlyjs='cdn')
	return 1


draw_chart_week()