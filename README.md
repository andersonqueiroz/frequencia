
<h1>Registro eletrônico de frequência para bolsistas</h1>

<p>Sistema atualmente sendo desenvolvido pela Coordenadoria de Apoio Tecnológico da Biblioteca Central Zila Mamede na UFRN, como
proposta de atualização da ferramenta atual, a fim de facilitar o processo de registro de frequência, cadastro de justificativas de ausência,
consulta de relatório mensal e de calendário da unidade.</p>

<h2>Requisitos</h2>

<ul>
  <li>Python 3</li>
  <li>Apache (mod_wsgi) / Nginx</li>
  <li>PostgreSQL / MySQL / Oracle</li>
</ul>

<h2>Instalação</h2>

<p>Para a realização do deploy no ambiente desejado, será necessária a instalação dos pacotes por meio do pip:</p>

<code>
pip install -r requirements.txt
</code>
<br>
<p>A criação dos grupos de usuários se dá via manager do Django, dentro do ambiente virtual (venv):</p>

<code>
  python ./manage.py instalacao
</code>
