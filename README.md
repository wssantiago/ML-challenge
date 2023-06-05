# ML-challenge
ML modelling stripts and a FastAPI application for ML model monitoring (using python:3.10.4)
 
### Instalação
Ao clonar este repositório, navegue para o diretório [./](./) (root) e crie um python virtual environment. No Windows, pode-se utilizar os seguintes comandos no terminal:
 
```
python -m venv venv
```
 
Esse comando cria o ambiente virtual com o nome de *venv* e para ativá-lo basta rodar o seguinte comando, também no Windows:
 
```
.\venv\Scripts\activate
```

Para instalar o ambiente virtual nas configurações locais do Jupyter, pode-se utilizar o comando a seguir:

```
python -m ipykernel install --user --name=venv
```

#### Dependências

Após ativar o ambiente virtual, utilize o ([pip](https://pip.pypa.io/en/stable/installation/)) para instalar as dependências contidas em [./requirements.txt](./requirements.txt). Para isso, estando no diretório [./](./), instale as dependências executando:

```
pip install -r requirements.txt
```

Agora, a API está pronta para ser executada, bem como os Jupyter Notebooks de modelagem ou o de teste da API. Para isso, navegue para o diretório [./app](./app) e inicie o app utilizando uvicorn fazendo, por exemplo:

```
cd app
uvicorn main:app --host 0.0.0.0 --port 8080
```

##### Dockerfile

De maneira alternativa, a API pode ser executada localmente utilizando ```docker```. Para isso, basta clonar o repositório e navegar no terminal para o diretório raiz [./](./). Assim, pode-se utilizar os dois comandos a seguir e o app estará sendo executado na porta 8080 do localhost:

```
docker build -t ml-app .
docker run -d -p 8080:8080 ml-app
```

Uma vez rodando, pode-se utilizar o [notebook](./notebooks/api-requests/API.ipynb) para realizar as chamadas à API.


### API

Em [./app/main.py](./app/main.py) estão referenciados dois endpoints: "/performance/" e "/aderencia/".

1. /performance/{model}
   - Ao fazer uma requisição POST para o servidor, espera-se, também, um parâmetro para esse endpoint. Isso ocorre pelo fato de haver dois possíveis modelos para se monitorar performance: [./models/classifier.pkl](./models/classifier.pkl) e [./models/regressor.pkl](./models/regressor.pkl). Assim o usuário pode escolher entre ter como resposta sejam as métricas do classificador ou as do regressor.
   - Assim, deve-se definir na URL da requisição "performance/classifier" ou "performance/regressor". Algo diferente disso deve retornar métricas vazias.
   - O "body" da requisição para esse endpoint foi definido como ```dict```, já que serão passados os dados no formato JSON para serem determinadas as métricas.
   - O modelo de time series forecasting não está ainda sendo suportado nesse endpoint.
   
2. /adherence/{model}
   - Ao fazer uma requisição POST para esse endpoint, espera-se um "body" da requisição como um  ```dict``` (além do parâmetro referente ao modelo sobre o qual a análise de aderência será realizada). Esse dicionário contém uma chave com valor referente aos dados do dataset referência e uma outra chave com os dados do dataset o qual pode estar sofrendo data drifting.


### Performance

Ao enviar um POST para se calcular as ```evaluation``` e ```satisficing metrics``` do modelo referenciado no parâmetro do endpoint, o módulo [performance.py](./app/api/endpoints/performance.py) é o responsável por determinar tais respostas.

   - Inicialmente, é verificado se o parâmetro do endpoint correspondente à versão do modelo é adequado. Dessa maneira, o classificador ou regressor é lido utilizando *pickle*. Após isso, é utilizada a pipeline para realizar a predição do dataset passado no "body" da requisição.

   - Com os valores preditos, as métricas são calculadas, bem como a latência necessária para predição, e os resultados são retornados como resposta à requisição também como um JSON.


### Aderência

Ao enviar um POST para se calcular as métricas resultantes do teste estatístico Kolmogorov-Smirnov entre as bases da requisição e a de referência, o módulo [aderencia.py](./app/api/endpoints/aderencia.py) é o responsável por determinar tais valores.

   - Inicialmente, o modelo classificador (até então único suportado nesse endpoint) é lido utilizando *pickle*. Assim, o modelo determina as distribuições de probabilidades de classificação (score) de ambas bases de referência e requisição.

   - Com isso, utiliza-se [ks_2samp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html) para realizar o teste estatístico e as duas métricas *statistic* e *p-value* são colocadas em um dicionário e retornadas como resposta à requisição como um JSON.


### Pasta utils

   - Nessa pasta está um módulo frequentemente na API para fazer leitura de modelos e um realizar o splitting dos datasets em ```X_``` e ```y_```.


### Logging

   - Ao começar a executar localmente o servidor seguindo as instruções acima, é possível verificar algumas informações acerca do processamento das requisições feitas para a API utilizando ```logging``` da *standard library* de python. Essas informações são formatadas e adicionadas em um arquivo de log que será criado em ```./monitoring.log```.


### Jupyter Notebook

   - Em [./notebooks](./notebooks), encontram-se os scripts de Python utilizados para modelagem dos três modelos, bem como o script relativo à análise exploratória.




