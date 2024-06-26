import streamlit as st
import yfinance as yf
import pandas as pd
import pickle
import os
# import winsound

st.set_page_config(layout="wide",page_title="Stock Data Application",initial_sidebar_state="expanded")
st.title('Stock Data Application')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            </style>
            """
#To reduce the whitespace at the top of the page
st.markdown("""
        <style>
               section.block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.markdown(hide_st_style, unsafe_allow_html=True)


SYMBOLS=['20MICRONS', '21STCENMGM', '360ONE', '3IINFOLTD', '3MINDIA', '3PLAND', '5PAISA', '63MOONS',
        'A2ZINFRA', 'AAATECH', 'AAKASH', 'AAREYDRUGS', 'AARON', 'AARTECH', 'AARTIDRUGS', 'AARTIIND',
        'AARTIPHARM', 'AARTISURF', 'AARVEEDEN', 'AARVI', 'AAVAS', 'ABAN', 'ABB', 'ABBOTINDIA', 'ABCAPITAL',
        'ABFRL', 'ABMINTLLTD', 'ABSLAMC', 'ACC', 'ACCELYA', 'ACCURACY', 'ACE', 'ACEINTEG', 'ACI', 'ACL',
        'ACLGATI', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADFFOODS', 'ADL',
        'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES', 'AEGISCHEM', 'AEROFLEX', 'AETHER', 'AFFLE',
        'AGARIND', 'AGI', 'AGRITECH', 'AGROPHOS', 'AGSTRA', 'AHL', 'AHLADA', 'AHLEAST', 'AHLUCONT', 'AIAENG', 
        'AIIL', 'AIRAN', 'AIROLAM', 'AJANTPHARM', 'AJMERA', 'AJOONI', 'AKASH', 'AKG', 'AKI', 'AKSHAR',
        'AKSHARCHEM', 'AKSHOPTFBR', 'AKZOINDIA', 'ALANKIT', 'ALBERTDAVD', 'ALEMBICLTD', 'ALICON', 'ALKALI',
        'ALKEM', 'ALKYLAMINE', 'ALLCARGO', 'ALLSEC', 'ALMONDZ', 'ALOKINDS', 'ALPA', 'ALPHAGEO', 'ALPSINDUS',
        'AMBER', 'AMBICAAGAR', 'AMBIKCO', 'AMBUJACEM', 'AMDIND', 'AMIORG', 'AMJLAND', 'AMNPLST', 'AMRUTANJAN',
        'ANANDRATHI', 'ANANTRAJ', 'ANDHRAPAP', 'ANDHRSUGAR', 'ANGELONE', 'ANIKINDS', 'ANKITMETAL', 'ANMOL',
        'ANTGRAPHIC', 'ANUP', 'ANURAS', 'APARINDS', 'APCL', 'APCOTEXIND', 'APEX', 'APLAPOLLO', 'APLLTD',
        'APOLLO', 'APOLLOHOSP', 'APOLLOPIPE', 'APOLLOTYRE', 'APOLSINHOT', 'APTECHT', 'APTUS', 'ARCHIDPLY',
        'ARCHIES', 'ARE&M', 'ARENTERP', 'ARIES', 'ARIHANTCAP', 'ARIHANTSUP', 'ARMANFIN', 'AROGRANITE',
        'ARROWGREEN', 'ARSHIYA', 'ARSSINFRA', 'ARTEMISMED', 'ARTNIRMAN', 'ARVEE', 'ARVIND', 'ARVINDFASN',
        'ARVSMART', 'ASAHIINDIA', 'ASAHISONG', 'ASAL', 'ASALCBR', 'ASHAPURMIN', 'ASHIANA', 'ASHIMASYN',
        'ASHOKA', 'ASHOKAMET', 'ASHOKLEY', 'ASIANENE', 'ASIANHOTNR', 'ASIANPAINT', 'ASIANTILES', 'ASKAUTOLTD',
        'ASMS', 'ASPINWALL', 'ASTEC', 'ASTERDM', 'ASTRAL', 'ASTRAMICRO', 'ASTRAZEN', 'ASTRON', 'ATALREAL',
        'ATAM', 'ATFL', 'ATGL', 'ATL', 'ATLANTAA', 'ATUL', 'ATULAUTO', 'AUBANK', 'AURIONPRO', 'AUROPHARMA',
        'AURUM', 'AUSOMENT', 'AUTOAXLES', 'AUTOIND', 'AVADHSUGAR', 'AVALON', 'AVANTIFEED', 'AVG', 'AVONMORE',
        'AVROIND', 'AVTNPL', 'AWHCL', 'AWL', 'AXISBANK', 'AXISCADES', 'AXITA', 'AYMSYNTEX', 'AZAD', 'BAFNAPH',
        'BAGFILMS', 'BAIDFIN', 'BAJAJ-AUTO', 'BAJAJCON', 'BAJAJELEC', 'BAJAJFINSV', 'BAJAJHCARE', 'BAJAJHIND',
        'BAJAJHLDNG', 'BAJEL', 'BAJFINANCE', 'BALAJITELE', 'BALAMINES', 'BALAXI', 'BALKRISHNA', 'BALKRISIND',
        'BALMLAWRIE', 'BALPHARMA', 'BALRAMCHIN', 'BALUFORGE', 'BANARBEADS', 'BANARISUG', 'BANCOINDIA',
        'BANDHANBNK', 'BANG', 'BANKA', 'BANKBARODA', 'BANKINDIA', 'BANSWRAS', 'BARBEQUE', 'BASF', 'BASML',
        'BATAINDIA', 'BAYERCROP', 'BBL', 'BBOX', 'BBTC', 'BBTCL', 'BCLIND', 'BCONCEPTS', 'BDL', 'BEARDSELL',
        'BECTORFOOD', 'BEDMUTHA', 'BEL', 'BEML', 'BEPL', 'BERGEPAINT', 'BESTAGRO', 'BFINVEST', 'BFUTILITIE',
        'BGRENERGY', 'BHAGCHEM', 'BHAGERIA', 'BHAGYANGR', 'BHANDARI', 'BHARATFORG', 'BHARATGEAR', 'BHARATRAS',
        'BHARATWIRE', 'BHARTIARTL', 'BHARTIHEXA', 'BHEL', 'BIGBLOC', 'BIKAJI', 'BIL', 'BINANIIND', 'BIOCON',
        'BIOFILCHEM', 'BIRLACABLE', 'BIRLACORPN', 'BIRLAMONEY', 'BKMINDST', 'BLAL', 'BLBLIMITED', 'BLISSGVS',
        'BLKASHYAP', 'BLS', 'BLSE', 'BLUECHIP', 'BLUEDART', 'BLUEJET', 'BLUESTARCO', 'BODALCHEM', 'BOHRAIND',
        'BOMDYEING', 'BOROLTD', 'BORORENEW', 'BOSCHLTD', 'BPCL', 'BPL', 'BRIGADE', 'BRITANNIA', 'BRNL', 'BROOKS',
        'BSE', 'BSHSL', 'BSL', 'BSOFT', 'BTML', 'BURNPUR', 'BUTTERFLY', 'BVCL', 'BYKE', 'CALSOFT', 'CAMLINFINE',
        'CAMPUS', 'CAMS', 'CANBK', 'CANFINHOME', 'CANTABIL', 'CAPACITE', 'CAPITALSFB', 'CAPLIPOINT', 'CAPTRUST',
        'CARBORUNIV', 'CAREERP', 'CARERATING', 'CARTRADE', 'CARYSIL', 'CASTROLIND', 'CCHHL', 'CCL', 'CDSL', 'CEATLTD',
        'CELEBRITY', 'CELLO', 'CENTENKA', 'CENTEXT', 'CENTRALBK', 'CENTRUM', 'CENTUM', 'CENTURYPLY', 'CENTURYTEX',
        'CERA', 'CEREBRAINT', 'CESC', 'CGCL', 'CGPOWER', 'CHALET', 'CHAMBLFERT', 'CHEMBOND', 'CHEMCON', 'CHEMFAB',
        'CHEMPLASTS', 'CHENNPETRO', 'CHEVIOT', 'CHOICEIN', 'CHOLAFIN', 'CHOLAHLDNG', 'CIEINDIA', 'CIGNITITEC', 
        'CINELINE', 'CINEVISTA', 'CIPLA', 'CLEAN', 'CLEDUCATE', 'CLSEL', 'CMSINFO', 'COALINDIA', 'COASTCORP', 
        'COCHINSHIP', 'COFFEEDAY', 'COFORGE', 'COLPAL', 'COMPUSOFT', 'COMSYN', 'CONCOR', 'CONCORDBIO', 'CONFIPET',
        'CONSOFINVT', 'CONTROLPR', 'CORALFINAC', 'CORDSCABLE', 'COROMANDEL', 'COSMOFIRST', 'COUNCODOS', 'CRAFTSMAN',
        'CREATIVE', 'CREATIVEYE', 'CREDITACC', 'CREST', 'CRISIL', 'CROMPTON', 'CROWN', 'CSBBANK', 'CSLFINANCE', 
        'CTE', 'CUB', 'CUBEXTUB', 'CUMMINSIND', 'CUPID', 'CYBERMEDIA', 'CYBERTECH', 'CYIENT', 'CYIENTDLM', 'DABUR',
        'DALBHARAT', 'DALMIASUG', 'DAMODARIND', 'DANGEE', 'DATAMATICS', 'DATAPATTNS', 'DAVANGERE', 'DBCORP', 'DBL',
        'DBOL', 'DBREALTY', 'DBSTOCKBRO', 'DCAL', 'DCBBANK', 'DCI', 'DCM', 'DCMFINSERV', 'DCMNVL', 'DCMSHRIRAM',
        'DCMSRIND', 'DCW', 'DCXINDIA', 'DECCANCE', 'DEEPAKFERT', 'DEEPAKNTR', 'DEEPENR', 'DEEPINDS', 'DELHIVERY',
        'DELPHIFX', 'DELTACORP', 'DELTAMAGNT', 'DEN', 'DENORA', 'DEVIT', 'DEVYANI', 'DGCONTENT', 'DHAMPURSUG', 
        'DHANBANK', 'DHANI', 'DHANUKA', 'DHARMAJ', 'DHRUV', 'DHUNINV', 'DIACABS', 'DIAMINESQ', 'DIAMONDYD',
        'DICIND', 'DIGIDRIVE', 'DIGISPICE', 'DIGJAMLMTD', 'DIL', 'DISHTV', 'DIVGIITTS', 'DIVISLAB', 'DIXON',
        'DJML', 'DLF', 'DLINKINDIA', 'DMART', 'DMCC', 'DNAMEDIA', 'DODLA', 'DOLATALGO', 'DOLLAR', 'DOLPHIN', 
        'DOMS', 'DONEAR', 'DPABHUSHAN', 'DPSCLTD', 'DPWIRES', 'DRCSYSTEMS', 'DREAMFOLKS', 'DREDGECORP', 'DRREDDY',
        'DSSL', 'DTIL', 'DUCON', 'DVL', 'DWARKESH', 'DYCL', 'DYNAMATECH', 'DYNPRO', 'E2E', 'EASEMYTRIP', 'ECLERX',
        'EDELWEISS', 'EDUCOMP', 'EICHERMOT', 'EIDPARRY', 'EIFFL', 'EIHAHOTELS', 'EIHOTEL', 'EIMCOELECO', 'EKC',
        'ELDEHSG', 'ELECON', 'ELECTCAST', 'ELECTHERM', 'ELGIEQUIP', 'ELGIRUBCO', 'ELIN', 'EMAMILTD', 'EMAMIPAP', 
        'EMAMIREAL', 'EMIL', 'EMKAY', 'EMMBI', 'EMSLIMITED', 'EMUDHRA', 'ENDURANCE', 'ENERGYDEV', 'ENGINERSIN',
        'ENIL', 'ENTERO', 'EPACK', 'EPIGRAL', 'EPL', 'EQUIPPP', 'EQUITASBNK', 'ERIS', 'EROSMEDIA', 'ESABINDIA', 
        'ESAFSFB', 'ESCORTS', 'ESSARSHPNG', 'ESSENTIA', 'ESTER', 'ETHOSLTD', 'EUROTEXIND', 'EVEREADY', 'EVERESTIND',
        'EXCEL', 'EXCELINDUS', 'EXICOM', 'EXIDEIND', 'EXPLEOSOL', 'EXXARO', 'FACT', 'FAIRCHEMOR', 'FAZE3Q', 'FCL',
        'FCONSUMER', 'FCSSOFT', 'FDC', 'FEDERALBNK', 'FEDFINA', 'FEL', 'FELDVR', 'FIBERWEB', 'FIEMIND', 'FILATEX',
        'FILATFASH', 'FINCABLES', 'FINEORG', 'FINOPB', 'FINPIPE', 'FIVESTAR', 'FLAIR', 'FLEXITUFF', 'FLFL', 
        'FLUOROCHEM', 'FMGOETZE', 'FMNL', 'FOCUS', 'FOODSIN', 'FORCEMOT', 'FORTIS', 'FOSECOIND', 'FSC', 'FSL', 
        'FUSION', 'GABRIEL', 'GAEL', 'GAIL', 'GALAXYSURF', 'GALLANTT', 'GANDHAR', 'GANDHITUBE', 'GANECOS', 'GANESHBE',
        'GANESHHOUC', 'GANGAFORGE', 'GANGESSECU', 'GARFIBRES', 'GATECH', 'GATECHDVR', 'GATEWAY', 'GAYAHWS', 'GAYAPROJ',
        'GEECEE', 'GEEKAYWIRE', 'GENCON', 'GENESYS', 'GENSOL', 'GENUSPAPER', 'GENUSPOWER', 'GEOJITFSL', 'GEPIL', 
        'GESHIP', 'GET&D', 'GFLLIMITED', 'GHCL', 'GHCLTEXTIL', 'GICHSGFIN', 'GICRE', 'GILLANDERS', 'GILLETTE', 
        'GINNIFILA', 'GIPCL', 'GKWLIMITED', 'GLAND', 'GLAXO', 'GLENMARK', 'GLFL', 'GLOBAL', 'GLOBALVECT', 'GLOBE',
        'GLOBUSSPR', 'GLOSTERLTD', 'GLS', 'GMBREW', 'GMDCLTD', 'GMMPFAUDLR', 'GMRINFRA', 'GMRP&UI', 'GNA', 'GNFC', 
        'GOACARBON', 'GOCLCORP', 'GOCOLORS', 'GODFRYPHLP', 'GODHA', 'GODREJAGRO', 'GODREJCP', 'GODREJIND', 'GODREJPROP',
        'GOENKA', 'GOKEX', 'GOKUL', 'GOKULAGRO', 'GOLDIAM', 'GOLDTECH', 'GOODLUCK', 'GOPAL', 'GOYALALUM', 'GPIL', 'GPPL',
        'GPTHEALTH', 'GPTINFRA', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GRAVITA', 'GREAVESCOT', 'GREENLAM', 'GREENPANEL',
        'GREENPLY', 'GREENPOWER', 'GRINDWELL', 'GRINFRA', 'GRMOVER', 'GROBTEA', 'GRPLTD', 'GRSE', 'GRWRHITECH', 'GSFC',
        'GSLSU', 'GSPL', 'GSS', 'GTECJAINX', 'GTL', 'GTLINFRA', 'GTPL', 'GUFICBIO', 'GUJALKALI', 'GUJAPOLLO', 'GUJGASLTD', 
        'GUJRAFFIA', 'GULFOILLUB', 'GULFPETRO', 'GULPOLY', 'GVKPIL', 'GVPTECH', 'HAL', 'HAPPSTMNDS', 'HAPPYFORGE', 'HARDWYN', 
        'HARIOMPIPE', 'HARRMALAYA', 'HARSHA', 'HATHWAY', 'HATSUN', 'HAVELLS', 'HAVISHA', 'HBLPOWER', 'HBSL', 'HCC', 'HCG',
        'HCL-INSYS', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HDIL', 'HEADSUP', 'HECPROJECT', 'HEG', 'HEIDELBERG', 
        'HEMIPROP', 'HERANBA', 'HERCULES', 'HERITGFOOD', 'HEROMOTOCO', 'HESTERBIO', 'HEUBACHIND', 'HEXATRADEX', 'HFCL',
        'HGINFRA', 'HGS', 'HIKAL', 'HIL', 'HILTON', 'HIMATSEIDE', 'HINDALCO', 'HINDCOMPOS', 'HINDCON', 'HINDCOPPER', 
        'HINDMOTORS', 'HINDOILEXP', 'HINDPETRO', 'HINDUNILVR', 'HINDWAREAP', 'HINDZINC', 'HIRECT', 'HISARMETAL', 
        'HITECH', 'HITECHCORP', 'HITECHGEAR', 'HLEGLAS', 'HLVLTD', 'HMAAGRO', 'HMT', 'HMVL', 'HNDFDS', 
        'HOMEFIRST', 'HONASA', 'HONAUT', 'HONDAPOWER', 'HOVS', 'HPAL', 'HPIL', 'HPL', 'HSCL', 'HTMEDIA', 'HUBTOWN', 'HUDCO', 
        'HUHTAMAKI', 'HYBRIDFIN', 'IBREALEST', 'IBULHSGFIN', 'ICDSLTD', 'ICEMAKE', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI',
        'ICIL', 'ICRA', 'IDBI', 'IDEA', 'IDEAFORGE', 'IDFC', 'IDFCFIRSTB', 'IEL', 'IEX', 'IFBAGRO', 'IFBIND', 'IFCI', 'IFGLEXPOR',
        'IGARASHI', 'IGL', 'IGPL', 'IIFL', 'IIFL-RE', 'IIFLSEC', 'IITL', 'IKIO', 'IL&FSENGG', 'IL&FSTRANS', 'IMAGICAA', 'IMFA',
        'IMPAL', 'IMPEXFERRO', 'INCREDIBLE', 'INDBANK', 'INDHOTEL', 'INDIACEM', 'INDIAGLYCO', 'INDIAMART', 'INDIANB', 'INDIANCARD',
        'INDIANHUME', 'INDIASHLTR', 'INDIGO', 'INDIGOPNTS', 'INDNIPPON', 'INDOAMIN', 'INDOBORAX', 'INDOCO', 'INDORAMA', 'INDOSTAR',
        'INDOTECH', 'INDOTHAI', 'INDOWIND', 'INDRAMEDCO', 'INDSWFTLAB', 'INDSWFTLTD', 'INDTERRAIN', 'INDUSINDBK', 'INDUSTOWER',
        'INFIBEAM', 'INFOBEAN', 'INFY', 'INGERRAND', 'INNOVACAP', 'INOXGREEN', 'INOXINDIA', 'INOXWIND', 'INSECTICID', 'INTELLECT',
        'INTENTECH', 'INTLCONV', 'INVENTURE', 'IOB', 'IOC', 'IOLCP', 'IONEXCHANG', 'IPCALAB', 'IPL', 'IRB', 'IRCON', 'IRCTC',
        'IREDA', 'IRFC', 'IRIS', 'IRISDOREME', 'IRMENERGY', 'ISEC', 'ISFT', 'ISGEC', 'ISMTLTD', 'ITC', 'ITDC', 'ITDCEM', 'ITI',
        'IVC', 'IVP', 'IWEL', 'IZMO', 'J&KBANK', 'JAGRAN', 'JAGSNPHARM', 'JAIBALAJI', 'JAICORPLTD', 'JAIPURKURT', 'JAMNAAUTO', 
        'JASH', 'JAYAGROGN', 'JAYBARMARU', 'JAYNECOIND', 'JAYSREETEA', 'JBCHEPHARM', 'JBMA', 'JCHAC', 'JETAIRWAYS', 'JETFREIGHT',
        'JGCHEM', 'JHS', 'JINDALPHOT', 'JINDALPOLY', 'JINDALSAW', 'JINDALSTEL', 'JINDRILL', 'JINDWORLD', 'JIOFIN', 'JISLDVREQS',
        'JISLJALEQS', 'JITFINFRA', 'JKCEMENT', 'JKIL', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JLHL', 'JMA', 'JMFINANCIL', 'JNKINDIA',
        'JOCIL', 'JPASSOCIAT', 'JPOLYINVST', 'JPPOWER', 'JSFB', 'JSL', 'JSWENERGY', 'JSWHL', 'JSWINFRA', 'JSWSTEEL', 'JTEKTINDIA',
        'JTLIND', 'JUBLFOOD', 'JUBLINDS', 'JUBLINGREA', 'JUBLPHARMA', 'JUNIPER', 'JUSTDIAL', 'JWL', 'JYOTHYLAB', 'JYOTICNC',
        'JYOTISTRUC', 'KABRAEXTRU', 'KAJARIACER', 'KAKATCEM', 'KALAMANDIR', 'KALYANI', 'KALYANIFRG', 'KALYANKJIL', 'KAMATHOTEL',
        'KAMDHENU', 'KAMOPAINTS', 'KANANIIND', 'KANORICHEM', 'KANPRPLA', 'KANSAINER', 'KAPSTON', 'KARMAENG', 'KARURVYSYA',
        'KAUSHALYA', 'KAVVERITEL', 'KAYA', 'KAYNES', 'KBCGLOBAL', 'KCP', 'KCPSUGIND', 'KDDL', 'KEC', 'KECL', 'KEEPLEARN',
        'KEI', 'KELLTONTEC', 'KERNEX', 'KESORAMIND', 'KEYFINSERV', 'KFINTECH', 'KHADIM', 'KHAICHEM', 'KHAITANLTD', 'KHANDSE',
        'KICL', 'KILITCH', 'KIMS', 'KINGFA', 'KIOCL', 'KIRIINDUS', 'KIRLOSBROS', 'KIRLOSENG', 'KIRLOSIND', 'KIRLPNU', 'KITEX', 
        'KKCL', 'KMSUGAR', 'KNRCON', 'KOHINOOR', 'KOKUYOCMLN', 'KOLTEPATIL', 'KOPRAN', 'KOTAKBANK', 'KOTARISUG', 'KOTHARIPET',
        'KOTHARIPRO', 'KPIGREEN', 'KPIL', 'KPITTECH', 'KPRMILL', 'KRBL', 'KREBSBIO', 'KRIDHANINF', 'KRISHANA', 'KRITI', 'KRITIKA',
        'KRITINUT', 'KRSNAA', 'KRYSTAL', 'KSB', 'KSCL', 'KSHITIJPOL', 'KSL', 'KSOLVES', 'KTKBANK', 'KUANTUM', 'LAGNAM', 'LAKPRE',
        'LAL', 'LALPATHLAB', 'LAMBODHARA', 'LANCORHOL', 'LANDMARK', 'LAOPALA', 'LASA', 'LATENTVIEW', 'LATTEYS', 'LAURUSLABS', 
        'LAXMICOT', 'LAXMIMACH', 'LCCINFOTEC', 'LEMONTREE', 'LEXUS', 'LFIC', 'LGBBROSLTD', 'LGBFORGE', 'LGHL', 'LIBAS', 'LIBERTSHOE',
        'LICHSGFIN', 'LICI', 'LIKHITHA', 'LINC', 'LINCOLN', 'LINDEINDIA', 'LLOYDSENGG', 'LLOYDSME', 'LODHA', 'LOKESHMACH', 
        'LORDSCHLO', 'LOTUSEYE', 'LOVABLE', 'LOYALTEX', 'LPDC', 'LT', 'LTF', 'LTFOODS', 'LTIM', 'LTTS', 'LUMAXIND', 'LUMAXTECH',
        'LUPIN', 'LUXIND', 'LXCHEM', 'LYKALABS', 'LYPSAGEMS', 'M&M', 'M&MFIN', 'MAANALU', 'MACPOWER', 'MADHAV', 'MADHUCON',
        'MADRASFERT', 'MAGADSUGAR', 'MAGNUM', 'MAHABANK', 'MAHAPEXLTD', 'MAHASTEEL', 'MAHEPC', 'MAHESHWARI', 'MAHLIFE', 'MAHLOG',
        'MAHSCOOTER', 'MAHSEAMLES', 'MAITHANALL', 'MALLCOM', 'MALUPAPER', 'MANAKALUCO', 'MANAKCOAT', 'MANAKSIA', 'MANAKSTEEL',
        'MANALIPETC', 'MANAPPURAM', 'MANGALAM', 'MANGCHEFER', 'MANGLMCEM', 'MANINDS', 'MANINFRA', 'MANKIND', 'MANOMAY', 'MANORAMA',
        'MANORG', 'MANUGRAPH', 'MANYAVAR', 'MAPMYINDIA', 'MARALOVER', 'MARATHON', 'MARICO', 'MARINE', 'MARKSANS', 'MARSHALL', 
        'MARUTI', 'MASFIN', 'MASKINVEST', 'MASTEK', 'MATRIMONY', 'MAWANASUG', 'MAXESTATES', 'MAXHEALTH', 'MAXIND', 'MAYURUNIQ',
        'MAZDA', 'MAZDOCK', 'MBAPL', 'MBECL', 'MBLINFRA', 'MCDOWELL-N', 'MCL', 'MCLEODRUSS', 'MCX', 'MEDANTA', 'MEDIASSIST',
        'MEDICAMEQ', 'MEDICO', 'MEDPLUS', 'MEGASOFT', 'MEGASTAR', 'MELSTAR', 'MENONBE', 'MEP', 'METALFORGE', 'METROBRAND',
        'METROPOLIS', 'MFSL', 'MGEL', 'MGL', 'MHLXMIRU', 'MHRIL', 'MICEL', 'MIDHANI', 'MINDACORP', 'MINDTECK', 'MIRCELECTR', 
        'MIRZAINT', 'MITCON', 'MITTAL', 'MKPL', 'MMFL', 'MMP', 'MMTC', 'MODIRUBBER', 'MODISONLTD', 'MODTHREAD', 'MOHITIND', 
        'MOIL', 'MOKSH', 'MOL', 'MOLDTECH', 'MOLDTKPAC', 'MONARCH', 'MONTECARLO', 'MOREPENLAB', 'MOTHERSON', 'MOTILALOFS', 'MOTISONS',
        'MOTOGENFIN', 'MPHASIS', 'MPSLTD', 'MRF', 'MRO-TEK', 'MRPL', 'MSPL', 'MSTCLTD', 'MSUMI', 'MTARTECH', 'MTEDUCARE', 'MTNL',
        'MUFIN', 'MUFTI', 'MUKANDLTD', 'MUKKA', 'MUKTAARTS', 'MUNJALAU', 'MUNJALSHOW', 'MURUDCERA', 'MUTHOOTCAP', 'MUTHOOTFIN',
        'MUTHOOTMF', 'MVGJL', 'NACLIND', 'NAGAFERT', 'NAGREEKCAP', 'NAGREEKEXP', 'NAHARCAP', 'NAHARINDUS', 'NAHARPOLY', 'NAHARSPING', 'NAM-INDIA', 'NARMADA', 'NATCOPHARM', 'NATHBIOGEN', 'NATIONALUM', 'NAUKRI', 'NAVA', 'NAVINFLUOR', 'NAVKARCORP', 'NAVNETEDUL', 'NAZARA', 'NBCC', 'NBIFIN', 'NCC', 'NCLIND', 'NDGL', 'NDL', 'NDLVENTURE', 'NDRAUTO', 'NDTV', 'NECCLTD', 'NECLIFE', 'NELCAST', 'NELCO', 'NEOGEN', 'NESCO', 'NESTLEIND', 'NETWEB', 'NETWORK18', 'NEULANDLAB', 'NEWGEN', 'NEXTMEDIA', 'NFL', 'NGIL', 'NGLFINE', 'NH', 'NHPC', 'NIACL', 'NIBL', 'NIITLTD', 'NIITMTS', 'NILAINFRA', 'NILASPACES', 'NILKAMAL', 'NINSYS', 'NIPPOBATRY', 'NIRAJ', 'NIRAJISPAT', 'NITCO', 'NITINSPIN', 'NITIRAJ', 'NKIND', 'NLCINDIA', 'NMDC', 'NOCIL', 'NOIDATOLL', 'NORBTEAEXP', 'NOVAAGRI', 'NRAIL', 'NRBBEARING', 'NRL', 'NSIL', 'NSLNISP', 'NTPC', 'NUCLEUS', 'NURECA', 'NUVAMA', 'NUVOCO', 'NYKAA', 'OAL', 'OBCL', 'OBEROIRLTY', 'OCCL', 'OFSS', 'OIL', 'OILCOUNTUB', 'OLECTRA', 'OMAXAUTO', 'OMAXE', 'OMINFRAL', 'OMKARCHEM', 'ONELIFECAP', 'ONEPOINT', 'ONGC', 'ONMOBILE', 'ONWARDTEC', 'OPTIEMUS', 'ORBTEXP', 'ORCHPHARMA', 'ORICONENT', 'ORIENTALTL', 'ORIENTBELL', 'ORIENTCEM', 'ORIENTCER', 'ORIENTELEC', 'ORIENTHOT', 'ORIENTLTD', 'ORIENTPPR', 'ORISSAMINE', 'ORTINLAB', 'OSIAHYPER', 'OSWALAGRO', 'OSWALGREEN', 'OSWALSEEDS', 'PAGEIND', 'PAISALO', 'PAKKA', 'PALASHSECU', 'PALREDTEC', 'PANACEABIO', 'PANACHE', 'PANAMAPET', 'PANSARI', 'PAR', 'PARACABLES', 'PARADEEP', 'PARAGMILK', 'PARAS', 'PARASPETRO', 'PARKHOTELS', 'PARSVNATH', 'PASUPTAC', 'PATANJALI', 'PATELENG', 'PATINTLOG', 'PAVNAIND', 'PAYTM', 'PCBL', 'PCJEWELLER', 'PDMJEPAPER', 'PDSL', 'PEARLPOLY', 'PEL', 'PENIND', 'PENINLAND', 'PERSISTENT', 'PETRONET', 'PFC', 'PFIZER', 'PFOCUS', 'PFS', 'PGEL', 'PGHH', 'PGHL', 'PGIL', 'PHOENIXLTD', 'PIDILITIND', 'PIGL', 'PIIND', 'PILANIINVS', 'PILITA', 'PIONEEREMB', 'PITTIENG', 'PIXTRANS', 'PKTEA', 'PLASTIBLEN', 'PLATIND', 'PLAZACABLE', 'PNB', 'PNBGILTS', 'PNBHOUSING', 'PNC', 'PNCINFRA', 'POCL', 'PODDARHOUS', 'PODDARMENT', 'POKARNA', 'POLICYBZR', 'POLYCAB', 'POLYMED', 'POLYPLEX', 'PONNIERODE', 'POONAWALLA', 'POWERGRID', 'POWERINDIA', 'POWERMECH', 'PPAP', 'PPL', 'PPLPHARMA', 'PRAENG', 'PRAJIND', 'PRAKASH', 'PRAKASHSTL', 'PRAXIS', 'PRECAM', 'PRECOT', 'PRECWIRE', 'PREMEXPLN', 'PREMIERPOL', 'PRESTIGE', 'PRICOLLTD', 'PRIMESECU', 'PRINCEPIPE', 'PRITI', 'PRITIKAUTO', 'PRIVISCL', 'PROZONER', 'PRSMJOHNSN', 'PRUDENT', 'PRUDMOULI', 'PSB', 'PSPPROJECT', 'PTC', 'PTCIL', 'PTL', 'PUNJABCHEM', 'PURVA', 'PVP', 'PVRINOX', 'PVSL', 'PYRAMID', 'QUESS', 'QUICKHEAL', 'RACE', 'RADAAN', 'RADHIKAJWE', 'RADIANTCMS', 'RADICO', 'RADIOCITY', 'RAILTEL', 'RAIN', 'RAINBOW', 'RAJESHEXPO', 'RAJMET', 'RAJRATAN', 'RAJRILTD', 'RAJSREESUG', 'RAJTV', 'RALLIS', 'RAMANEWS', 'RAMAPHO', 'RAMASTEEL', 'RAMCOCEM', 'RAMCOIND', 'RAMCOSYS', 'RAMKY', 'RAMRAT', 'RANASUG', 'RANEENGINE', 'RANEHOLDIN', 'RATEGAIN', 'RATNAMANI', 'RATNAVEER', 'RAYMOND', 'RBA', 'RBL', 'RBLBANK', 'RBZJEWEL', 'RCF', 'RCOM', 'RECLTD', 'REDINGTON', 'REDTAPE', 'REFEX', 'REGENCERAM', 'RELAXO', 'RELCHEMQ', 'RELIANCE', 'RELIGARE', 'RELINFRA', 'REMSONSIND', 'RENUKA', 'REPCOHOME', 'REPL', 'REPRO', 'RESPONIND', 'RGL', 'RHFL', 'RHIM', 'RHL', 'RICOAUTO', 'RIIL', 'RISHABH', 'RITCO', 'RITES', 'RKDL', 'RKEC', 'RKFORGE', 'RKSWAMY', 'RML', 'ROHLTD', 'ROLEXRINGS', 'ROLLT', 'ROML', 'ROSSARI', 'ROSSELLIND', 'ROTO', 'ROUTE', 'RPGLIFE', 'RPOWER', 'RPPINFRA', 'RPPL', 'RPSGVENT', 'RPTECH', 'RRKABEL', 'RSSOFTWARE', 'RSWM', 'RSYSTEMS', 'RTNINDIA', 'RTNPOWER', 'RUBYMILLS', 'RUCHINFRA', 'RUCHIRA', 'RUPA', 'RUSHIL', 'RUSTOMJEE', 'RVHL', 'RVNL', 'S&SPOWER', 'SABEVENTS', 'SABTNL', 'SADBHAV', 'SADBHIN', 'SADHNANIQ', 'SAFARI', 'SAGARDEEP', 'SAGCEM', 'SAH', 'SAHYADRI', 'SAIL', 'SAKAR', 'SAKHTISUG', 'SAKSOFT', 'SAKUMA', 'SAKUMA-RE', 'SALASAR', 'SALONA', 'SALSTEEL', 'SALZERELEC', 'SAMBHAAV', 'SAMHI', 'SAMPANN', 'SANDESH', 'SANDHAR', 'SANDUMA', 'SANGAMIND', 'SANGHIIND', 'SANGHVIMOV', 'SANGINITA', 'SANOFI', 'SANSERA', 'SAPPHIRE', 'SARDAEN', 'SAREGAMA', 'SARLAPOLY', 'SARVESHWAR', 'SASKEN', 'SASTASUNDR', 'SATIA', 'SATIN', 'SATINDLTD', 'SAURASHCEM', 'SBC', 'SBCL', 'SBFC', 'SBGLP', 'SBICARD', 'SBILIFE', 'SBIN', 'SCHAEFFLER', 'SCHAND', 'SCHNEIDER', 'SCI', 'SCILAL', 'SCPL', 'SDBL', 'SEAMECLTD', 'SECMARK', 'SECURCRED', 'SECURKLOUD', 'SEJALLTD', 'SELAN', 'SELMC', 'SEMAC', 'SENCO', 'SEPC', 'SEQUENT', 'SERVOTECH', 'SESHAPAPER', 'SETCO', 'SEYAIND', 'SFL', 'SGIL', 'SGL', 'SHAH', 'SHAHALLOYS', 'SHAILY', 'SHAKTIPUMP', 'SHALBY', 'SHALPAINTS', 'SHANKARA', 'SHANTI', 'SHANTIGEAR', 'SHARDACROP', 'SHARDAMOTR', 'SHAREINDIA', 'SHEMAROO', 'SHILPAMED', 'SHIVALIK', 'SHIVAMAUTO', 'SHIVAMILLS', 'SHIVATEX', 'SHK', 'SHOPERSTOP', 'SHRADHA', 'SHREDIGCEM', 'SHREECEM', 'SHREEPUSHK', 'SHREERAMA', 'SHRENIK', 'SHREYANIND', 'SHREYAS', 'SHRIPISTON', 'SHRIRAMFIN', 'SHRIRAMPPS', 'SHYAMCENT', 'SHYAMMETL', 'SHYAMTEL', 'SICALLOG', 'SIEMENS', 'SIGACHI', 'SIGIND', 'SIGMA', 'SIGNATURE', 'SIGNPOST', 'SIKKO', 'SIL', 'SILGO', 'SILINV', 'SILLYMONKS', 'SILVERTUC', 'SIMBHALS', 'SIMPLEXINF', 'SINCLAIR', 'SINDHUTRAD', 'SINTERCOM', 'SIRCA', 'SIS', 'SIYSIL', 'SJS', 'SJVN', 'SKFINDIA', 'SKIPPER', 'SKMEGGPROD', 'SKYGOLD', 'SMARTLINK', 'SMCGLOBAL', 'SMLISUZU', 'SMLT', 'SMSLIFE', 'SMSPHARMA', 'SNOWMAN', 'SOBHA', 'SOFTTECH', 'SOLARA', 'SOLARINDS', 'SOMANYCERA', 'SOMATEX', 'SOMICONVEY', 'SONACOMS', 'SONAMLTD', 'SONATSOFTW', 'SOTL', 'SOUTHBANK', 'SOUTHWEST', 'SPAL', 'SPANDANA', 'SPARC', 'SPCENET', 'SPECIALITY', 'SPENCERS', 'SPIC', 'SPLIL', 'SPLPETRO', 'SPMLINFRA', 'SPORTKING', 'SPYL', 'SREEL', 'SRF', 'SRGHFL', 'SRHHYPOLTD', 'SRM', 'SRPL', 'SSWL', 'STAR', 'STARCEMENT', 'STARHEALTH', 'STARPAPER', 'STARTECK', 'STCINDIA', 'STEELCAS', 'STEELCITY', 'STEELXIND', 'STEL', 'STERTOOLS', 'STLTECH', 'STOVEKRAFT', 'STYLAMIND', 'STYRENIX', 'SUBEXLTD', 'SUBROS', 'SUDARSCHEM', 'SUKHJITS', 'SULA', 'SUMEETINDS', 'SUMICHEM', 'SUMIT', 'SUMMITSEC', 'SUNCLAY', 'SUNDARAM', 'SUNDARMFIN', 'SUNDARMHLD', 'SUNDRMBRAK', 'SUNDRMFAST', 'SUNFLAG', 'SUNPHARMA', 'SUNTECK', 'SUNTV', 'SUPERHOUSE', 'SUPERSPIN', 'SUPRAJIT', 'SUPREMEENG', 'SUPREMEIND', 'SUPREMEINF', 'SUPRIYA', 'SURAJEST', 'SURANASOL', 'SURANAT&P', 'SURYALAXMI', 'SURYAROSNI', 'SURYODAY', 'SUTLEJTEX', 'SUULD', 'SUVEN', 'SUVENPHAR', 'SUVIDHAA', 'SUZLON', 'SVLL', 'SVPGLOB', 'SWANENERGY', 'SWARAJENG', 'SWELECTES', 'SWSOLAR', 'SYMPHONY', 'SYNCOMF', 'SYNGENE', 'SYRMA', 'TAINWALCHM', 'TAJGVK', 'TAKE', 'TALBROAUTO', 'TANLA', 'TARACHAND', 'TARAPUR', 'TARC', 'TARMAT', 'TARSONS', 'TASTYBITE', 'TATACHEM', 'TATACOMM', 'TATACONSUM', 'TATAELXSI', 'TATAINVEST', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TATATECH', 'TATVA', 'TBZ', 'TCI', 'TCIEXP', 'TCLCONS', 'TCNSBRANDS', 'TCPLPACK', 'TCS', 'TDPOWERSYS', 'TEAMLEASE', 'TECHIN', 'TECHM', 'TECHNOE', 'TECILCHEM', 'TEGA', 'TEJASNET', 'TEMBO', 'TERASOFT', 'TEXINFRA', 'TEXMOPIPES', 'TEXRAIL', 'TFCILTD', 'TFL', 'TGBHOTELS', 'THANGAMAYL', 'THEINVEST', 'THEJO', 'THEMISMED', 'THERMAX', 'THOMASCOOK', 'THOMASCOTT', 'THYROCARE', 'TI', 'TIDEWATER', 'TIIL', 'TIINDIA', 'TIJARIA', 'TIL', 'TIL-RE', 'TIMESGTY', 'TIMETECHNO', 'TIMKEN', 'TIPSFILMS', 'TIPSINDLTD', 'TIRUMALCHM', 'TIRUPATIFL', 'TITAGARH', 'TITAN', 'TMB', 'TNPETRO', 'TNPL', 'TNTELE', 'TOKYOPLAST', 'TORNTPHARM', 'TORNTPOWER', 'TOTAL', 'TOUCHWOOD', 'TPHQ', 'TPLPLASTEH', 'TRACXN', 'TREEHOUSE', 'TREJHARA', 'TREL', 'TRENT', 'TRF', 'TRIDENT', 'TRIGYN', 'TRIL', 'TRITURBINE', 'TRIVENI', 'TRU', 'TTKHLTCARE', 'TTKPRESTIG', 'TTL', 'TTML', 'TV18BRDCST', 'TVSELECT', 'TVSHLTD', 'TVSMOTOR', 'TVSSCS', 'TVSSRICHAK', 'TVTODAY', 'TVVISION', 'UBL', 'UCAL', 'UCOBANK', 'UDAICEMENT', 'UDS', 'UFLEX', 'UFO', 'UGARSUGAR', 'UGROCAP', 'UJJIVANSFB', 'ULTRACEMCO', 'UMAEXPORTS', 'UMANGDAIRY', 'UMESLTD', 'UNICHEMLAB', 'UNIDT', 'UNIENTER', 'UNIINFO', 'UNIONBANK', 'UNIPARTS', 'UNITECH', 'UNITEDPOLY', 'UNITEDTEA', 'UNIVASTU', 'UNIVCABLES', 'UNIVPHOTO', 'UNOMINDA', 'UPL', 'URAVI', 'URJA', 'USHAMART', 
        'USK', 'UTIAMC', 'UTKARSHBNK', 'UTTAMSUGAR', 'V2RETAIL', 'VADILALIND', 'VAIBHAVGBL', 'VAISHALI', 
        'VAKRANGEE', 'VALIANTLAB', 'VALIANTORG', 'VARDHACRLC', 'VARDMNPOLY', 'VARROC', 'VASCONEQ', 'VASWANI', 'VBL', 
        'VEDL', 'VENKEYS', 'VENUSPIPES', 'VENUSREM', 'VERANDA', 'VERTOZ', 'VESUVIUS', 'VETO', 'VGUARD', 
        'VHL', 'VIDHIING', 'VIJAYA', 'VIJIFIN', 'VIKASECO', 'VIKASLIFE', 'VIMTALABS', 'VINATIORGA', 
        'VINDHYATEL', 'VINEETLAB', 'VINNY', 'VINYLINDIA', 'VIPCLOTHNG', 'VIPIND', 'VIPULLTD', 'VIRINCHI', 
        'VISAKAIND', 'VISHNU', 'VISHWARAJ', 'VIVIDHA', 'VLEGOV', 'VLSFINANCE', 'VMART', 'VOLTAMP', 
        'VOLTAS', 'VPRPL', 'VRLLOG', 'VSSL', 'VSTIND', 'VSTL', 'VSTTILLERS', 'VTL', 'WABAG', 'WALCHANNAG',
        'WANBURY', 'WEALTH', 'WEBELSOLAR', 'WEIZMANIND', 'WEL', 'WELCORP', 'WELENT', 'WELINV', 'WELSPUNLIV', 
        'WENDT', 'WESTLIFE', 'WEWIN', 'WHEELS', 'WHIRLPOOL', 'WILLAMAGOR', 'WINDLAS', 'WINDMACHIN', 'WINSOME', 
        'WIPL', 'WIPRO', 'WOCKPHARMA', 'WONDERLA', 'WORTH', 'WSI', 'WSTCSTPAPR', 'XCHANGING', 'XELPMOC',
        'XPROINDIA', 'YAARI', 'YASHO', 'YATHARTH', 'YATRA', 'YESBANK', 'YUKEN', 'ZAGGLE', 'ZEEL', 'ZEELEARN', 'ZEEMEDIA', 
        'ZENITHEXPO', 'ZENITHSTL', 'ZENSARTECH', 'ZENTEC', 'ZFCVINDIA', 'ZIMLAB', 'ZODIAC', 'ZODIACLOTH', 'ZOMATO', 'ZOTA', 
        'ZUARI', 'ZUARIIND', 'ZYDUSLIFE', 'ZYDUSWELL']

SYMBOL=SYMBOLS

def getData(interval='1mo',period='max',start_date=None,end_date=None,symbolsList=SYMBOL):
    print('No of symbols: ',len(symbolsList))
    intervals=['1d','1wk', '1mo', '3mo']
    periods=['10y', 'ytd', 'max']
    if interval not in intervals:
        raise Exception(f'interval argument is not valid!!\n{intervals}')
    if period not in periods:
        raise Exception(f'period argument is not valid!!\n{periods}')
    
    
    print(f'Getting data for all {len(symbolsList)} stocks!!')
    STOCK_DATA={}
    SYMBOLS=[f'{i}.NS' for i in symbolsList]
    try:
        
        if start_date is not None and end_date is not None:
            DATA=yf.download(SYMBOLS,interval=interval,period=period,start=start_date,end=end_date,threads = True)
        elif start_date is not None and end_date is None:
            DATA=yf.download(SYMBOLS,interval=interval,period=period,start=start_date,threads = True)
        elif start_date is None and end_date is not None:
            DATA=yf.download(SYMBOLS,interval=interval,period=period,end=end_date,threads = True)
        elif start_date is None and end_date is None:
            DATA=yf.download(SYMBOLS,interval=interval,period=period,threads = True)     
    except Exception as e:
        try:
            print('Exception in downloading! Trying again')
            DATA=yf.download(SYMBOLS,interval=interval,period=period,threads = True)
        except Exception as e:
            print(f'Error in getting {interval} data of stock {s}\n','-'*100)
            print(e)
    
    if DATA.shape[1]>7:   
        data=DATA.T.swaplevel().unstack()
        grouped=data.groupby(by=['High', 'Open', 'Volume', 'Adj Close', 'Low', 'Close'],level=0)
        
        for s in SYMBOLS: 
            try:
                STOCK_DATA[s.replace('.NS','')]=grouped.get_group(s).T.unstack().droplevel(axis=1,level=0).dropna(subset=['Close','Open','High','Low'],axis=0)

            except Exception as e:
                print(f'Error in getting data of stock {s}\n')
                print(e,'-'*100)
    else:
        STOCK_DATA[SYMBOLS[0].replace('.NS','')]=DATA
    return STOCK_DATA

def get_index_data(interval='1wk',period='max'):
    MATCHING_SYMBOLS={'NIFTY_50': '^NSEI','NIFTY_BANK': '^NSEBANK','NIFTY_FIN_SERVICE': 'NIFTY_FIN_SERVICE.NS','NIFTY_IT': '^CNXIT',
 'NIFTY_MIDCAP_100': 'NIFTY_MIDCAP_100.NS','NIFTY_MIDCAP_50': '^NSEMDCP50','NIFTY_100': '^CNX100','NIFTY_500': '^CRSLDX',
 'NIFTY_AUTO': '^CNXAUTO','NIFTY_PSU_BANK': '^CNXPSUBANK','NIFTY_COMMODITIES': '^CNXCMDT','NIFTY_FMCG': '^CNXFMCG',
 'NIFTY_PVT_BANK': 'NIFTY_PVT_BANK.NS','NIFTY_METAL': '^CNXMETAL','NIFTY_ENERGY': '^CNXENERGY','NIFTY_MEDIA': '^CNXMEDIA',
 'NIFTY_INFRA': '^CNXINFRA','NIFTY_SERV_SECTOR': '^CNXSERVICE','NIFTY_REALTY': '^CNXREALTY','NIFTY_PSE': '^CNXPSE',
 'NIFTY_MID_LIQ_15': 'NIFTYMIDLIQ15.NS','NIFTY_NEXT_50': '^NSMIDCP','NIFTY_CONSUMPTION': '^CNXCONSUM','NIFTY_MNC': '^CNXMNC',
 'NIFTY_DIV_OPPS_50': '^CNXDIVOP','NIFTY50_DIV_POINT': '^NSEDIV'}
    
    BENCHMARK_DATA={}
    # SYMBOLS={i:MATCHING_SYMBOLS[i] for i in benchmarkSymbolsList if i.upper() in MATCHING_SYMBOLS.keys()}
    SYMBOLS=MATCHING_SYMBOLS.copy()
    try:
        Data=yf.download(list(SYMBOLS.values()),interval=interval,period=period,threads = True)
    except Exception as e:
        # print('Error in getting Data')
        print(f'Error in getting {interval} data of stock {s}\n','-'*100)
        print(e)
    try:   
        
        data=Data.T.swaplevel().unstack()
        grouped=data.groupby(by=['High', 'Open', 'Volume', 'Adj Close', 'Low', 'Close'],level=0)
    
    
        for s,v in SYMBOLS.items(): 
            try:
                BENCHMARK_DATA[s]=grouped.get_group(v).T.unstack().droplevel(axis=1,level=0).dropna(subset=['Close','Open','High','Low'],axis=0)

            except Exception as e:
                print(f'Error in getting data of stock {s}\n')
                print(e,'-'*100)
    except Exception as e:
        print(e)
        print("length of benchmark data is",len(SYMBOLS))
        for s,v in SYMBOLS.items():
            BENCHMARK_DATA[s]=Data
    return BENCHMARK_DATA

if __name__ == "__main__":
    Monthly_Data=st.button('Monthly Data',key=1)
    if Monthly_Data:
        st.download_button("Download Monthly Data",data=pickle.dumps(getData(interval='1mo',period='max',symbolsList=SYMBOL)),file_name='MONTHLY_DATA.pkl')
    Weekly_Data=st.button('Weekly Data',key=2)
    if Weekly_Data:
        st.download_button("Download Weekly Data",data=pickle.dumps(getData(interval='1wk',period='max',symbolsList=SYMBOL)),file_name='WEEKLY_DATA.pkl')
    Daily_Data=st.button('Daily Data',key=3)
    if Daily_Data:
        DATA={}
        l=len(SYMBOL)//4
        data1=getData(interval='1d',period='max',symbolsList=SYMBOL[:l])
        data2=getData(interval='1d',period='max',symbolsList=SYMBOL[l:(l*2)])
        data3=getData(interval='1d',period='max',symbolsList=SYMBOL[(l*2):(l*3)])
        data4=getData(interval='1d',period='max',symbolsList=SYMBOL[(l*3):])
        DATA.update(data1)
        DATA.update(data2)
        DATA.update(data3)
        DATA.update(data4)
        st.download_button("Download Daily Data",data=pickle.dumps(DATA),file_name='DAILY_DATA.pkl')
                
    Weekly_Index_Data=st.button('Weekly Index Data',key=4)   
    if Weekly_Index_Data:
        st.download_button("Download Weekly Index Data",data=pickle.dumps(get_index_data(interval='1wk',period='max')),file_name='WEEKLY_INDEX_DATA.pkl')
    Daily_Index_Data=st.button('Daily Index Data',key=5)    
    if Daily_Index_Data:
        st.download_button("Download Daily Index Data",data=pickle.dumps(get_index_data(interval='1d',period='max')),file_name='DAILY_INDEX_DATA.pkl')
    st.success('Data Gathered')
# def Store_Data(period='max',symbolsList=(SYMBOL[:(lenSYMBOL))//4)]:
    
#     try:
#         MONTHLY_DATA=getData(interval='1mo',period=period,symbolsList=symbolsList)
#         WEEKLY_DATA=getData(interval='1wk',period=period,symbolsList=symbolsList)
#         DAILY_DATA=getData(interval='1d',period=period,symbolsList=symbolsList)
#         WEEKLY_INDEX_DATA=get_index_data(interval='1wk',period=period)
#         DAILY_INDEX_DATA=get_index_data(interval='1d',period=period)
#         if 'temp' not in os.listdir('.'):
#             os.mkdir('./temp')
#         with open('./temp/MONTHLY_DATA.pkl','wb') as f:
#             pickle.dump(MONTHLY_DATA,f)
#         with open('./temp/WEEKLY_DATA.pkl','wb') as f:
#             pickle.dump(WEEKLY_DATA,f)
#         with open('./temp/DAILY_DATA.pkl','wb') as f:
#             pickle.dump(DAILY_DATA,f)
#         with open('./temp/WEEKLY_INDEX_DATA.pkl','wb') as f:
#             pickle.dump(WEEKLY_INDEX_DATA,f)
#         with open('./temp/DAILY_INDEX_DATA.pkl','wb') as f:
#             pickle.dump(DAILY_INDEX_DATA,f)
#     except Exception as e:
#         print("ERROR: Could not download the data!")
#         print(e)
#         print(e)
#         return False
#     print("Downloaded Data Successfully!")
#     return True

