import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Read the training loss data from the provided text
data = '''1 	1.904200
2 	2.448400
3 	2.013900
4 	1.897700
5 	1.836800
6 	1.884300
7 	1.868500
8 	1.929300
9 	1.590700
10 	1.492500
11 	1.487400
12 	1.491400
13 	1.484700
14 	1.357300
15 	1.434400
16 	1.462300
17 	1.326100
18 	1.316700
19 	1.197000
20 	1.085400
21 	1.020000
22 	1.101900
23 	1.059300
24 	1.041000
25 	0.964200
26 	0.967700
27 	0.836500
28 	0.861100
29 	0.829500
30 	0.905400
31 	0.775800
32 	0.767600
33 	0.632700
34 	0.556400
35 	0.631000
36 	0.446800
37 	0.528500
38 	0.612300
39 	0.410300
40 	0.384400
41 	0.377200
42 	0.302600
43 	0.670200
44 	0.625100
45 	0.399400
46 	0.319300
47 	0.425000
48 	0.553600
49 	0.313200
50 	0.207100
51 	0.415600
52 	0.319600
53 	0.225700
54 	0.216100
55 	0.592400
56 	0.182200
57 	0.155200
58 	0.228700
59 	0.179400
60 	0.325900
61 	0.172300
62 	0.141300
63 	0.201600
64 	0.139900
65 	0.182400
66 	0.232800
67 	0.141900
68 	0.313700
69 	0.090400
70 	0.098400
71 	0.108100
72 	0.140500
73 	0.134900
74 	0.170000
75 	0.105200
76 	0.223000
77 	0.150500
78 	0.117900
79 	0.232700
80 	0.288800
81 	0.071500
82 	0.139800
83 	0.053700
84 	0.080200
85 	0.339100
86 	0.074700
87 	0.031000
88 	0.155200
89 	0.099300
90 	0.435700
91 	0.240400
92 	0.162300
93 	0.127800
94 	0.129000
95 	0.097000
96 	0.234200
97 	0.127300
98 	0.089700
99 	0.124800
100 	0.078700
101 	0.056200
102 	0.063700
103 	0.162400
104 	0.125500
105 	0.065500
106 	0.140700
107 	0.076300
108 	0.060500
109 	0.096600
110 	0.066100
111 	0.068300
112 	0.066500
113 	0.039900
114 	0.026700
115 	0.113100
116 	0.065000
117 	0.146300
118 	0.048300
119 	0.032100
120 	0.081800
121 	0.074600
122 	0.089500
123 	0.081400
124 	0.025200
125 	0.112200
126 	0.051700
127 	0.120800
128 	0.047800
129 	0.151700
130 	0.059900
131 	0.022400
132 	0.035900
133 	0.023000
134 	0.119700
135 	0.009600
136 	0.043800
137 	0.088100
138 	0.029700
139 	0.042200
140 	0.023500
141 	0.077400
142 	0.026700
143 	0.126700
144 	0.058100
145 	0.046600
146 	0.022800
147 	0.051600
148 	0.022700
149 	0.047200
150 	0.113300
151 	0.043000
152 	0.020900
153 	0.031700
154 	0.097900
155 	0.038900
156 	0.083800
157 	0.107200
158 	0.037000
159 	0.071900
160 	0.033700
161 	0.016900
162 	0.076000
163 	0.022900
164 	0.077400
165 	0.025200
166 	0.053800
167 	0.050500
168 	0.055400
169 	0.047900
170 	0.023400
171 	0.037300
172 	0.037000
173 	0.024700
174 	0.016900
175 	0.034700
176 	0.044800
177 	0.018600
178 	0.032300
179 	0.033100
180 	0.031800
181 	0.034800
182 	0.029400
183 	0.040600
184 	0.023200
185 	0.017600
186 	0.015700
187 	0.027500
188 	0.042800
189 	0.046300
190 	0.010100
191 	0.044300
192 	0.057600
193 	0.014600
194 	0.020000
195 	0.019700
196 	0.038900
197 	0.016000
198 	0.017500
199 	0.028100
200 	0.008700
201 	0.027900
202 	0.019800
203 	0.022000
204 	0.008000
205 	0.015300
206 	0.026300
207 	0.047700
208 	0.039800
209 	0.022600
210 	0.024300
211 	0.018400
212 	0.016400
213 	0.018700
214 	0.028400
215 	0.017800
216 	0.037800
217 	0.018200
218 	0.011900
219 	0.034400
220 	0.010700
221 	0.025200
222 	0.014300
223 	0.021100
224 	0.028500
225 	0.011500
226 	0.009900
227 	0.034700
228 	0.035200
229 	0.058300
230 	0.014100
231 	0.013500
232 	0.024900
233 	0.015000
234 	0.014700
235 	0.014300
236 	0.012900
237 	0.011300
238 	0.022700
239 	0.021100
240 	0.017500
241 	0.012900
242 	0.025400
243 	0.015200
244 	0.017500
245 	0.017600
246 	0.010200
247 	0.018700
248 	0.012600
249 	0.040000
250 	0.018500
251 	0.009000
252 	0.010400
253 	0.011700
254 	0.019400
255 	0.012300
256 	0.020500
257 	0.034200
258 	0.022800
259 	0.036200
260 	0.010700
261 	0.009100
262 	0.029100
263 	0.018400
264 	0.018500
265 	0.008200
266 	0.024900
267 	0.010600
268 	0.013000
269 	0.014500
270 	0.013000
271 	0.010300
272 	0.021500
273 	0.009000
274 	0.023600
275 	0.024600
276 	0.021100
277 	0.010200
278 	0.017700
279 	0.025300
280 	0.015700
281 	0.009500
282 	0.009000
283 	0.010300
284 	0.014000
285 	0.019000
286 	0.008900
287 	0.027000
288 	0.011600
289 	0.009900
290 	0.011800
291 	0.016000
292 	0.023500
293 	0.022400
294 	0.025400
295 	0.018100
296 	0.014800
297 	0.016700
298 	0.022500
299 	0.020700
300 	0.008900
301 	0.010400
302 	0.007300
303 	0.008300
304 	0.008100
305 	0.013600
306 	0.014700
307 	0.014000
308 	0.015300
309 	0.015100
310 	0.017400
311 	0.009300
312 	0.013800
313 	0.027700
314 	0.015300
315 	0.008000
316 	0.023700
317 	0.011200
318 	0.027600
319 	0.015500
320 	0.012600
321 	0.019100
322 	0.020200
323 	0.007500
324 	0.013400
325 	0.011700
326 	0.015500
327 	0.010500
328 	0.019700
329 	0.016400
330 	0.010200'''

# Convert the data to a list of floats
loss_values = [float(line.split()[1]) for line in data.split('\n') if line.strip()]
steps = list(range(1, len(loss_values) + 1))

# Calculate moving average (window size = 5)
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

moving_avg = moving_average(loss_values, 5)
moving_avg_steps = steps[4:]  # Adjust x-axis for moving average

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('LLM Fine-tuning Training Analysis \n', fontsize=16, fontweight='bold')

# Main plot - Training Loss
ax1.plot(steps, loss_values, 'o-', color='#4A56E2', alpha=0.7, markersize=4, label='Training Loss')
ax1.plot(moving_avg_steps, moving_avg, '-', color='#FF6B6B', linewidth=2, label='5-Step Moving Average')

# Add epoch markers
steps_per_epoch = 33
for epoch in range(1, 11):
    step_num = epoch * steps_per_epoch
    if step_num <= len(steps):
        ax1.axvline(x=step_num, color='gray', linestyle='--', alpha=0.5)
        ax1.text(step_num, ax1.get_ylim()[1]*0.95, f'Epoch {epoch}', rotation=90, verticalalignment='top',
                 horizontalalignment='right', color='gray')

# Set up the first subplot  
ax1.set_xlabel('Training Step')
ax1.set_ylabel('Loss') 
ax1.set_ylim(0, max(loss_values)*1.1)
ax1.set_xlim(0, len(steps))
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper right')
ax1.set_title('Training Loss Over Time', fontsize=14)

# Annotate important points
ax1.annotate(f'Initial Loss: {loss_values[0]:.2f}', xy=(1, loss_values[0]), xytext=(1, max(loss_values)*0.9), 
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)
ax1.annotate(f'Final Loss: {loss_values[-1]:.2f}', xy=(len(steps), loss_values[-1]), xytext=(len(steps)*0.9, min(loss_values)*2), 
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)
ax1.annotate(f'Lowest Loss: {min(loss_values):.3f}', xy=(loss_values.index(min(loss_values))+1, min(loss_values)), xytext=(len(steps)*0.7, min(loss_values)*1.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)

# Create a table of training metrics in the second subplot
ax2.axis('tight')  
ax2.axis('off')

metrics_data = [
    ["GPU", "Tesla T4"],
    ["Total Training Time", "89.43 minutes"],
    ["Peak Memory Usage", "13.766 GB (93.39% of max)"], 
    ["Total Steps", "330"],
    ["Batch Size", "8 (2 per device × 4 accumulation steps)"],
    ["Trainable Parameters", "41,943,040"],
    ["Training Examples", "264"]
]

table = ax2.table(
    cellText=metrics_data,
    colLabels=["Metric", "Value"],
    loc='center',
    cellLoc='left',
    colWidths=[0.4, 0.6]    
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)  
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header
        cell.set_text_props(fontproperties=dict(weight='bold'))  
        cell.set_facecolor('#e0e0e0')
    elif row % 2 == 1:  # Alternating row colors
        cell.set_facecolor('#f5f5f5')

ax2.set_title('Training Configuration Metrics', fontsize=14)

# Calculate some statistics for the text box
initial_loss = loss_values[0]
final_loss = loss_values[-1] 
min_loss = min(loss_values)
min_loss_step = loss_values.index(min_loss) + 1
reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100

# Add a text box with analysis 
textstr = '\n'.join([
    'Loss Analysis:',
    f'• Initial Loss: {initial_loss:.2f}', 
    f'• Final Loss: {final_loss:.2f}',
    f'• Minimum Loss: {min_loss:.3f} (Step {min_loss_step})',
    f'• Reduction: {reduction_pct:.1f}%',
    '',
    'The loss curve indicates successful training with a 99.5% reduction in loss.',
    'Training converged very well, with loss consistently decreasing over 10 epochs.'
])

props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)  
ax1.text(0.6, 0.97, textstr, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.subplots_adjust(hspace=0.3)

plt.savefig('llm_training_analysis_updated.png', dpi=300, bbox_inches='tight')
plt.show()