# JSON unified format integrated NEURON simulator
This program is wrapper of NEURON simulator().  
in neuron, you wright channel physical properties, or point processes with NMODL, and all the other with hoc/python.  
But all the other composed from form of the cell, number of cells, their connection, external stimulus, recording, and so on.  
That make the simulation programs chaotic, because each researchers has been write it as they like. Especially in IO process.  
In this program, you can write form of the cell, number of cell, their connection, external stimulus, recording respectively.  
Setting of number of cell, their connection, external stimulus, recording is JSON format.  

## Requirement
This program requires below  
python 2.7.x  
numpy  
Neuron 7.5 with paranrn, nrnpy  

## インストール
git cloneしてください。  
git clone後、直下のmeta.jsonファイルを開き、"nrnpy-path": ""の右のダブルクオーテーション内に、nrnpyのインストールディレクトリを入れてください。  
> `{`  
> `  "nrnpy-path": "your nrnpy directory"`  
> `}`  

## 実行
実行するファイルはparallelNeuronSimulation.pyです。  
例えばtestdata/HHsingle_example/run.jsonを指定してシミュレーションを実行する場合は  
`python parallelNeuronSimulation.py -s testdata/HHsingle_exsample/run.json`  
となります。  
MPI並列化したい場合は,例えば8プロセスだと  
`mpirun -n 8 python parallelNeuronSimulation.py -s testdata/HHsingle_exsample/run.json`  
となります。  
出力結果はpickle dump形式でresult下の実行日時のディレクトリに出力されます。  

## 使い方
1. 実行について
現状オプションは-sのみです。  
実行時指定ファイルはschema/run_schema.jsonに従った記法で表記してください。  

2. 細胞配置について
実行時指定ファイルの"dynamics_def_path"によって指定されるjsonファイルは細胞の個数配置についてを記述します。  
schema/dynamics_schema.jsonにしたがった記法で表記してください。  
"celltype"で指定した形態の細胞を生成します。このとき"params"のメンバー変数は形態インスタンス生成時の第三引数に渡されます。詳しくは細胞形態についての項を参照してください。  
"cellname"という項を指定した場合、各細胞に名前が付与されます。これは任意です。"cellname"の有無によらず、このファイルの各細胞に通し番号が上から0,1,2,...と与えられ、固有の"cellid"になります。  

3. 細胞形態について
細胞形態はクラスオブジェクトとしてpythonプログラムにより作成します。ただし、クラスはメンバ変数にcellという辞書型の変数を用意しください。  
クラスの \_\_init\_\_はselfの他に第一引数～第三引数までを取ります。第一引数は固有のcellid、cellname_module.jsonの"opt"および、"dynamics_def_path"の"params"がそれぞれ第二第三引数に該当します。  
` class HHmodel:`  
`    def __init__(self, index, opt={}, params={}):`  
`        self.index = index`  
`        self.cell={}`  
作成したセクションはcellにその名前をキーとして代入してください。コレ以降のファイルにおける["section"]["name"]は、cell["name"]に対応するセクションを呼び出します。  
自身で作成した細胞形態クラスをシミュレーションで使いたい場合は,cellname_module.jsonにクラス名とパスを追記してください。
それ以外に関しては通常のneuron with pythonの記法と同一です。  

4. ネットワークについて
実行時指定ファイルの"connection_def_path"によって指定されるjsonファイルは細胞間の接続についてを記述します。  
schema/connection_schema.jsonに従った記法で表記してください。  

5. 外部刺激について
実行時指定ファイルの"stim_setting_path"によって指定されるjsonファイルは細胞への外部刺激についてを記述します。  
schema/stim_schema.jsonに従った記法で表記してください。  

6. 記録について
実行時指定ファイルの"record_setting_path"によって指定されるjsonファイルは細胞を記録する方法についてを記述します。  
schema/record_schema.jsonに従った記法で表記してください。  
