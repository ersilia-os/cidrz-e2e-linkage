import streamlit as st
from datetime import datetime
import random
import os

from e2elink.synthetic.tablegen.singletable import NaiveReferenceTableGenerator
from e2elink.synthetic.tablegen.linkedtable import ReferenceLinkedTables, find_ground_truth
from e2elink.synthetic.tablegen.transform import TableTransformer
from e2elink.synthetic.utils.saver import save_results

from e2elink.synthetic.misspell.simple import SimpleMisspell
from e2elink.synthetic.misspell.embedding import EmbeddingMisspell

simple_misspell = None
embedding_misspell = None

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

class Defaults():

    def __init__(self):
        self.defaults = {
            "dupl": [1, 10],
            "date_sorted": [True, False],
            "date_coverage": [90, 80, 100],
            "date_format": [0, 1, 2],
            "name_info": [0, 1],
            "name_from": [0, 1],
            "name_coverage": [95, 90, 100],
            "name_format": [0, 1, 2],
            "name_abbreviation_rate": [1, 10],
            "name_swapping_rate": [1, 10],
            "name_misspelling_rate": [10, 20, 30],
            "age_format": [0, 1, 2],
            "age_coverage": [90, 80, 100],
            "do_identifier": [False, True],
            "identifier_coverage": [10, 25, 50, 75, 90],
            "sex_format": [0, 1, 2, 3]
        }

    def default(self):
        return dict((k, v[0]) for k,v in self.defaults.items())

    def random(self):
        return dict((k, random.choice(v)) for k,v in self.defaults.items())

default = Defaults()

folder_name = st.sidebar.text_input("Folder name", value="")

# Source file
st.sidebar.title('Source file')

# Basics
src_size = st.sidebar.number_input(
    'Number of samples',
    min_value=10, max_value=100000,
    value=100
)
src_dupl = st.sidebar.slider(
    'Proportion of duplicates (%)',
    0, 100,
    10
)/100
src_visits = st.sidebar.slider(
    'Average visits',
    min_value=1.,
    max_value=5.,
    value=1.5,
    step=0.1
)

# Dates
st.sidebar.subheader("Date")
src_date_sorted = st.sidebar.checkbox(
   "Sorted dates",
   value = True
)
c01, c02 = st.sidebar.beta_columns(2)
src_date_lb = c01.date_input(
    "First visit",
    datetime.strptime("2017-01-01", "%Y-%m-%d")
)
src_date_lb = datetime.strftime(src_date_lb, "%Y-%m-%d")
src_date_ub = c02.date_input(
   "Last visit",
   datetime.strptime("2020-12-31", "%Y-%m-%d")
)
src_date_ub = datetime.strftime(src_date_ub, "%Y-%m-%d")
src_date_coverage = st.sidebar.slider(
   "Date coverage (%)",
   0, 100,
   90
)/100
c11, c12 = st.sidebar.beta_columns(2)
src_date_format = c11.selectbox(
   "Date format",
   ["2020-12-31",
    "31 Dec 2020",
    "31/12/20"],
    index = 0
)
if src_date_format == "2020-12-31":
    _df = "%Y-%m-%d"
elif src_date_format == "31 Dec 2020":
    _df = "%d %b %Y"
elif src_date_format == "31/12/20":
    _df = "%d/%m/%y"
else:
    pass
src_date_format = _df
src_date_missformat_rate = c12.slider(
   "Date missformat (%)",
   0, 100,
   10
)

# Names
st.sidebar.subheader("Name")
c21, c22 = st.sidebar.beta_columns(2)
src_name_info = c21.radio(
    'Name information',
    ["Full", "First & last"],
    index = 0
)
if src_name_info == "Full":
    src_split_full_name = False
else:
    src_split_full_name = True
src_name_from = c22.radio(
    'Name origin',
    ["Local", "Global"],
    index = 0
)
if src_name_from == "Local":
    src_local = True
else:
    src_local = False
src_female_prop = st.sidebar.slider(
    'Proportion of females (%)',
    0, 100,
    50
)/100
src_name_coverage = st.sidebar.slider(
    'Name coverage (%)',
    0, 100,
    98
)/100
c31, c32 = st.sidebar.beta_columns(2)
src_name_format = c31.selectbox(
    "Name format",
    ["John Smith",
     "john smith",
     "JOHN SMITH"],
     index = 0
)
if src_name_format == "John Smith":
    _nf = "title"
elif src_name_format == "john smith":
    _nf = "lower"
elif src_name_format == "JOHN SMITH":
    _nf = "upper"
else:
    pass
src_name_format = _nf
src_name_missformat_rate = c32.slider(
   "Name missformat (%)",
   0, 100,
   10
)/100
src_name_abbreviation_rate = c31.slider(
   "Abbreviation (%)",
   0, 100,
   5
)/100
src_name_swapping_rate = c32.slider(
   "Swapping (%)",
   0, 100,
   5
)/100
src_name_misspelling_rate = c31.slider(
  "Misspelling (%)",
  0, 100,
  10
)/100
src_name_misspelling_type = c32.radio(
   "Misspelling type",
   ["Fast", "Accurate"],
   index = 0
)

# Age
st.sidebar.subheader("Age")
c41, c42 = st.sidebar.beta_columns(2)
src_age_format = c41.radio(
    'Age format',
    ["Date of birth", "Year of birth", "Age"],
    index = 0
)
if src_age_format == "Date of birth":
     _af = "birth_date"
elif src_age_format == "Year of birth":
    _af = "birth_year"
elif src_age_format == "Age":
    _af = "age"
else:
    pass
src_age_format = _af
src_age_missformat_rate = c42.slider(
   "Age missformat (%)",
   0, 100,
   10
)/100
src_age_range = st.sidebar.slider(
    'Age range (95% CI)',
    0, 120,
    (15, 75)
)
src_age_lb = src_age_range[0]
src_age_ub = src_age_range[1]
src_age_coverage = st.sidebar.slider(
    'Age coverage (%)',
    0, 100,
    95
)/100

# Other
st.sidebar.subheader("Other")

# Identifier
src_do_identifier = st.sidebar.checkbox(
   'Identifier',
   value = True
)
if src_do_identifier:
    src_identifier_coverage = st.sidebar.slider(
        'Identifier coverage (%)',
        0, 100,
        25
    )/100
    src_identifier_type = None
else:
    src_identifier_coverage = 1.
    src_identifier_type = None

# Random choices
src_sex_format = random.choice(["lower_abbrv", "upper_abbrv", "lower", "title"])


# Target file

st.sidebar.title('Target file')

trg_size = st.sidebar.number_input(
    'Number of samples',
    10, 1000000,
    1000
)

# Linkage

st.sidebar.title('Ground truth')

exp_linkage_rate = st.sidebar.slider(
    'Expected linkage rate (%)',
    0, 100, 70
)/100

linkage_difficulty = st.sidebar.radio(
    'Linkage difficulty',
    ["Low", "High"]
)

# Compute

bc1, bc2, bc3 =st.beta_columns(3)
compute = bc1.button('Generate!')
refresh = bc2.button('Refresh')
if refresh:
    src_def = default.random()
    trg_def = default.random()

# Provisional
trg_identifier_type = None,
trg_local = src_local,
trg_date_lb = src_date_lb,
trg_date_ub = src_date_ub,
trg_age_lb = src_age_lb,
trg_age_ub = src_age_ub,
trg_female_prop = src_female_prop,
trg_dupl = 15


if not compute:
    with open(os.path.join(SCRIPT_PATH, "INSTRUCTIONS.md"), "r") as f:
        st.markdown(f.read())
else:
    bc3.button("Download")
    # Source generator
    src_gen = NaiveReferenceTableGenerator(
        identifier_type = src_identifier_type,
        local = src_local,
        date_lb = src_date_lb,
        date_ub = src_date_ub,
        age_lb = src_age_lb,
        age_ub = src_age_ub,
        female_prop = src_female_prop,
        duplicates_prop = src_dupl,
        average_visits = src_visits
    )
    # Target generator
    trg_gen = NaiveReferenceTableGenerator(
        identifier_type = trg_identifier_type,
        local = trg_local,
        date_lb = trg_date_lb,
        date_ub = trg_date_ub,
        age_lb = trg_age_lb,
        age_ub = trg_age_ub,
        female_prop = trg_female_prop
    )

    # Linked generator
    lt = ReferenceLinkedTables(src_gen, trg_gen)
    ref_data = lt.sample(src_size, trg_size, exp_linkage_rate)

    # Load misspelling if necessary
    if src_name_misspelling_type == "Fast":
        if simple_misspell is None:
            simple_misspell = SimpleMisspell()
        ms = simple_misspell
    if src_name_misspelling_type == "Accurate":
        if embedding_misspell is None:
            embedding_misspell = EmbeddingMisspell()
        ms = embedding_misspell

    # Transformers

    # Source table
    st.title("Source file")
    src_tf = TableTransformer(ref_data["src"])
    src_params = {
        "sort_by_date": src_date_sorted,
        "date_format": src_date_format,
        "swap_full_name": src_name_swapping_rate,
        "abbreviate_full_name": src_name_abbreviation_rate,
        "misspell_full_name": src_name_misspelling_rate,
        "misspell_type": src_name_misspelling_type,
        "misspeller": ms,
        "age_format": src_age_format,
        "name_format": src_name_format,
        "split_full_name": src_split_full_name,
        "shuffle_columns": False,
        "hide_identifier": not src_do_identifier,
        "identifier_coverage": src_identifier_coverage,
        "rename_columns": None,
        "date_coverage": src_date_coverage,
        "name_coverage": src_name_coverage,
        "age_coverage": src_age_coverage,
        "date_coverage": src_date_coverage,
        "sex_format": src_sex_format
    }
    src_tf.transform(src_params)
    src_uid = src_tf.uid
    src_data = src_tf.data.copy()
    st.dataframe(src_data)
    src_tf = src_tf.reset()

    # Target table
    st.title("Target file")
    trg_tf = TableTransformer(ref_data["trg"])
    trg_params = {
        "sort_by_date": False,
        "date_format": "%d/%m/%y",
        "swap_full_name": src_name_swapping_rate,
        "abbreviate_full_name": src_name_abbreviation_rate,
        "misspell_full_name": src_name_misspelling_rate,
        "misspell_type": src_name_misspelling_type,
        "misspeller": None,
        "age_format": "birth_date",
        "name_format": "upper",
        "split_full_name": True,
        "shuffle_columns": False,
        "hide_identifier": False,
        "identifier_coverage": 0.8,
        "rename_columns": None,
        "date_coverage": src_date_coverage,
        "name_coverage": src_name_coverage,
        "age_coverage": src_age_coverage,
        "date_coverage": src_date_coverage,
        "sex_format": "upper_abbrv"
    }
    trg_tf.transform(trg_params)
    trg_uid = trg_tf.uid
    trg_data = trg_tf.data.copy()
    st.dataframe(trg_data)
    trg_tf = trg_tf.reset()

    # Linkage file
    st.title("Ground truth")
    pairs = find_ground_truth(src_uid, trg_uid)
    st.dataframe(pairs)

    # Truth params
    truth_params = {
        "exp_linkage_rate": exp_linkage_rate
    }

    src_params["size"] = src_size
    trg_params["size"] = trg_size

    # Saver
    if folder_name:
        ROOT = "/Users/mduran/Desktop/"
        save_results(ROOT, folder_name, src_data, trg_data, pairs, src_params, trg_params, truth_params)
