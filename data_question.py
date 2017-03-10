import math
import operator
import numpy
import pandas as pd

# Update the file path here
filename_2014="./PartD_Prescriber_PUF_NPI_14/PartD_Prescriber_PUF_NPI_14.txt"
filename_2013="./PartD_Prescriber_PUF_NPI_13/PARTD_PRESCRIBER_PUF_NPI_13.txt"

summation=0
counter=0
errors=0
empty =0
prescription_len=[]
graph_total_claim = {}
graph_brand_claim = {}
graph_opioid={}
graph_antibiotic={}
graph_final={}
graph_state={}
stddev=[]
list_age_65 = []
list_lis = []
max_opioid_state = {}
bene_summation = 0
bene_counter = 0

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

#function for calculating the Pearson Coefficient
def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)

def question1(bene_count,bene_summation,bene_counter):
    try:
        bene_count = int(bene_count)
        if isinstance(bene_count,int):
            bene_summation += bene_count
            bene_counter += 1
        return bene_summation,bene_counter
    except:
        pass

def question5(val1,val2,val3):
    try:
        val1=int(val1)
        val2=int(val2)
        val3=int(val3)
        list_age_65.append(float(val1)/val3)
        list_lis.append(float(val2)/val3)
    except:
        pass

def question6(val1,val2,val3):
    try:
        state = str(val1).strip().upper()
        specialty = str(val2).replace(" ","_").lower()
        opioid = int(val3)

        max_opioid_state.setdefault(specialty,{})
        max_opioid_state[specialty].setdefault(state)
        if max_opioid_state[specialty][state]:
            temp = opioid + max_opioid_state[specialty][state].pop()
        else:
            temp = opioid
        max_opioid_state[specialty][state]=temp
    except:
        pass

with open(filename_2014) as f:
    next(f)
    for line in f:
        line = line.strip()
        words = line.split('\t')
        npi = words[0]
        bene_count=words[17]
        total_claim_count = words[18]
        total_day_supply = words[20]
        specialty_description=words[14]
        nppes_provider_state = words[12]
        brand_claim_count = words[27]
        opioid_bene_count = words[48]
        antibiotic_bene_count = words[52]
        bene_count_ge65 = words[21]
        lis_claim_count = words[42]
        opioid_day_supply = words[51]

        try: #question 1
            bene_count = int(bene_count)
            bene_summation, bene_counter = question1(bene_count,bene_summation,bene_counter)
        except:
            continue

        question5(bene_count_ge65,lis_claim_count,bene_count)
        question6(nppes_provider_state,specialty_description,opioid_day_supply)

        try:
            total_claim_count = int(total_claim_count)
            total_day_supply = int(total_day_supply)
            if brand_claim_count!="" and int(brand_claim_count)>10:
                key = str(specialty_description).strip().lower().replace(" ","_")
                key_state = nppes_provider_state.strip().upper()
                val_total = int(total_claim_count)
                val_brand = int(brand_claim_count)
                val_opioid = opioid_bene_count
                val_antibiotic = antibiotic_bene_count
                if val_opioid == "": val_opioid = 0
                if val_antibiotic == "": val_antibiotic = 0
                graph_total_claim.setdefault(key, set())
                graph_total_claim[key].add(int(val_total))
                graph_brand_claim.setdefault(key,set())
                graph_brand_claim[key].add(int(val_brand))
                graph_opioid.setdefault(key_state,set())
                graph_opioid[key_state].add(int(val_opioid))
                graph_antibiotic.setdefault(key_state,set())
                graph_antibiotic[key_state].add(int(val_antibiotic))
            if total_claim_count !=0:
                prescription_len.append(float(total_day_supply/total_claim_count))
        except Exception as e:
            print str(e)
            continue
        try:
            bene_count=int(bene_count)
            if bene_count!="":
                summation = summation+bene_count
                counter = counter+1
        except:
            continue

print "1.) The average number of beneficiaries per provider is %s.\n"%(bene_summation/bene_counter)
def median(lst):
    return numpy.median(numpy.array(lst))

print "2.) The median, in days, of the distribution of this value across all providers is %s days.\n"%median(prescription_len)
print "3.1) For each Specialty the fraction of drug claims that are for brand-name drugs. " \
      "Include only providers for whom the relevant information has not been suppressed, and " \
      "consider only specialties with at least 1000 total claims.\n"
for keys in graph_total_claim:
    if graph_total_claim[keys]>1000:
        graph_final.setdefault(keys,[])
        graph_final[keys].insert(0,sum(graph_total_claim[keys]))
for keys in graph_brand_claim:
    if graph_final[keys]:
        graph_final[keys].insert(1,sum(graph_brand_claim[keys]))
for keys in graph_final:
    try:
        val = round(float(graph_final[keys][1])/graph_final[keys][0],10)
        graph_final[keys]=val
        stddev.append(val)
    except:
        graph_final[keys] = 0
        stddev.append(val)
avg = float(sum(stddev))/len(stddev)

variance = map(lambda x: (x - avg)**2, stddev)

avg_variance = float(sum(variance))/len(variance)

standard_deviation = round(math.sqrt(avg_variance),10)

print graph_final
print "\n3.2) The standard deviation of these fractions is %s.\n"%standard_deviation
for keys in graph_opioid:
    graph_state.setdefault(keys,[])
    graph_state[keys].insert(0,sum(graph_opioid[keys]))
for keys in graph_antibiotic:
    if graph_state[keys]:
        graph_state[keys].insert(1,sum(graph_antibiotic[keys]))
min_ratio=max_ratio=0
for keys in graph_state:
    try:
        val = round(float(graph_state[keys][0])/graph_state[keys][1],10)
        if val<min_ratio: min_ratio=val
        if val>max_ratio: max_ratio=val
        graph_state[keys]=val
    except:
        graph_state[keys]=0
print "4.1) The ratio of beneficiaries with opioid prescriptions to beneficiaries with antibiotics prescriptions in each state.\n"
print graph_state
print "\n4.2) The difference between the largest and smallest ratios is %s.\n"%(max_ratio-min_ratio)
print "5.) The Pearson correlation coefficient between these values is %s. " \
      "Value shows negative linear correlation.\n"%pearson(list_age_65,list_lis)

print "6.) States which have surprisingly high supply of opioids, conditioned on specialty.\n"
for keys in max_opioid_state:
    print "%s - %s, "%(keys, max(max_opioid_state[keys].iteritems(),key=operator.itemgetter(1))[0]),

f_2014 = pd.read_csv(filename_2014, header= None ,escapechar=';', delimiter='\t', low_memory=False)
f_2013 = pd.read_csv(filename_2013, header= None,delimiter='\t', low_memory=False)

# both dataframes are merged but could not understand
# the question and what was to be calculated. The question language isn't clear.

merge_data = pd.merge(pd.DataFrame(f_2014), pd.DataFrame(f_2013),on=1) 

# Solutions
# 1.) The average number of beneficiaries per provider is 148.
# 
# 2.) The median, in days, of the distribution of this value across all providers is 29.0 days.
# 
# 3.1) For each Specialty the fraction of drug claims that are for brand-name drugs. Include only providers for whom the relevant information has not been suppressed, and consider only specialties with at least 1000 total claims.
# 
# {'clinical_psychologist': 0.162590879, 'vascular_surgery': 0.0595859776, 'health_maintenance_organization': 0.1859694783, 'crna': 0.1980154726, 'surgical_oncology': 0.1405695985, 'hospital_(dmercs_only)': 0.1326696358, 'psychologist_(billing_independently)': 0.1267184514, 'maxillofacial_surgery': 0.0308608646, 'pharmacy': 1.0, 'respite_care': 0.1569998924, 'plastic_surgery': 0.1440408783, 'military_health_care_provider': 0.3412526998, 'allergy/immunology': 0.2835989249, 'physical_medicine_and_rehabilitation': 0.1190213355, 'preventive_medicine': 0.2624181164, 'homeopath': 0.1689135607, 'hematology': 0.2017776943, 'unknown_physician_specialty_code': 0.2634884679, 'legal_medicine': 0.2063956988, 'ophthalmology': 0.4982080515, 'exclusive_provider_organization': 0.0705128205, 'general_surgery': 0.1852647604, 'chronic_disease_hospital': 0.1958867161, 'general_acute_care_hospital': 0.1767323586, 'licensed_clinical_social_worker': 0.1974195165, 'speech_language_pathologist': 0.2294952681, 'critical_care_(intensivists)': 0.4474172822, 'medical_oncology': 0.1294945962, 'substance_abuse_rehabilitation_facility': 0.2781456954, 'massage_therapist': 0.187755102, 'physical_therapist': 0.2042417199, 'public_health_welfare_agency': 0.35, 'licensed_vocational_nurse': 0.1421487603, 'social_worker': 0.1869328494, 'student_in_an_organized_health_care_education/training_program': 0.1377936542, 'dental_assistant': 0.1120689655, 'rheumatology': 0.1536001112, 'mass_immunization_roster_biller': 1.0, 'neurology': 0.1249858386, 'cardiac_surgery': 0.1494538188, 'snf_(dmercs_only)': 0.1777777778, 'neuropsychiatry': 0.1380416943, 'surgery': 0.1939043615, 'obstetrics/gynecology': 0.2281216315, 'registered_nurse': 0.1858063037, 'nuclear_medicine': 0.2575270826, 'home_health_aide': 0.325, 'licensed_practical_nurse': 0.19672805, 'medical_genetics': 0.4173913043, 'hospice_and_palliative_care': 0.2084219082, 'specialist': 0.205382558, 'rehabilitation_agency': 0.1861394048, 'occupational_therapy_assistant': 0.2791519435, 'pediatrics': 0.6585365854, 'radiation_oncology': 0.2315999878, 'gynecological/oncology': 0.1329694259, 'infectious_disease': 0.3768256894, 'hand_surgery': 0.0511461828, 'orthopaedic_surgery': 0.1677451043, 'pharmacy_technician': 0.7111111111, 'general_practice': 0.1587633473, 'case_management': 0.230958231, 'certified_nurse_midwife': 0.2014401989, 'counselor': 0.1647360328, 'pulmonary_disease': 0.3574283213, 'thoracic_surgery': 0.1433362496, 'technician/technologist': 0.6605504587, 'radiologic_technologist': 0.2137681159, 'sleep_medicine': 0.2507968487, 'internal_medicine': 0.1170780138, 'thoracic_surgery_(cardiothoracic_vascular_surgery)': 0.2488673645, 'medical_supply_company,_other': 0.2564102564, 'religious_nonmedical_nursing_personnel': 0.2768273717, 'emergency_medicine': 0.1907320893, 'podiatry': 0.1021986021, 'interventional_radiology': 0.173818435, 'independent_medical_examiner': 0.200575374, 'physical_medicine_&_rehabilitation': 0.2532751092, 'nutritionist': 0.13, 'audiologist_(billing_independently)': 0.512195122, 'psychoanalyst': 0.1508760545, 'anesthesiology': 0.1046618462, 'hematology/oncology': 0.1376424579, 'medical_genetics,_ph.d._medical_genetics': 0.159789644, 'radiology': 0.2432610125, 'urology': 0.1548324539, 'cardiac_electrophysiology': 0.189954554, 'interventional_cardiology': 0.1774996808, 'multispecialty_clinic/group_practice': 0.224642387, 'health_educator': 0.1780821918, 'preferred_provider_organization': 0.2013593883, 'family_practice': 0.1033853426, 'contractor': 0.1506653019, 'unknown_supplier/provider': 0.1397449522, 'osteopathic_manipulative_medicine': 0.2129676874, 'plastic_and_reconstructive_surgery': 0.0915511172, 'occupational_therapist': 0.274559194, 'diagnostic_radiology': 0.228382991, 'geriatric_medicine': 0.2071933596, 'dentist': 0.0783114636, 'clinic/center': 0.1908616287, 'technician': 0.1741935484, 'specialist/technologist,_other': 0.2192513369, 'sports_medicine': 0.1321163697, 'oral_&_maxillofacial_surgery': 0.035378124, 'chore_provider': 0.1721854305, 'family_medicine': 0.2028762467, 'personal_emergency_response_attendant': 0.1569734366, 'case_manager/care_coordinator': 0.2796181462, 'veterinarian': 0.2448979592, 'pain_management': 0.1149892137, 'addiction_medicine': 0.2377625154, 'clinical_neuropsychologist': 0.1689451132, 'specialist/technologist': 0.2666666667, 'neurological_surgery': 0.1561003797, 'geriatric_psychiatry': 0.1585961818, 'endocrinology': 0.3635574376, 'oral_surgery_(dentists_only)': 0.0220414662, 'dermatology': 0.0777945877, 'neurosurgery': 0.0661741397, 'community_health_worker': 0.1268353448, 'interventional_pain_management': 0.117836679, 'midwife': 0.2412022066, 'pathology': 0.2385114416, 'nephrology': 0.1777436216, 'physician_assistant': 0.1128122202, 'colorectal_surgery_(formerly_proctology)': 0.2282232521, 'obstetrics_&_gynecology': 0.226835443, 'hospitalist': 0.1747351075, 'midwife,_lay': 0.2203389831, 'cardiology': 0.1308796887, 'registered_dietician/nutrition_professional': 0.2659279778, 'behavioral_analyst': 0.236516576, 'ambulatory_surgical_center': 0.2692307692, 'orthopedic_surgery': 0.0650812701, 'certified_clinical_nurse_specialist': 0.1240758071, 'electrodiagnostic_medicine': 0.2365591398, 'pharmacist': 0.2195762242, 'anesthesiologist_assistants': 0.5098039216, 'residential_treatment_facility,_physical_disabilities': 0.2857142857, 'optometry': 0.5364042397, 'gastroenterology': 0.1964802923, 'driver': 0.1670513911, 'rehabilitation,_substance_use_disorder_unit': 0.1944444444, 'colon_&_rectal_surgery': 0.3037752414, 'clinical_pharmacology': 0.1736289844, 'acupuncturist': 0.210282343, 'emergency_medical_technician,_basic': 0.3717948718, 'naprapath': 0.1194379391, 'pediatric_medicine': 0.1947656553, 'psychiatry_&_neurology': 0.1013523979, 'genetic_counselor,_ms': 0.3216783217, 'adult_companion': 0.1114503817, 'naturopath': 0.2076983764, 'neuromusculoskeletal_medicine,_sports_medicine': 0.1570404223, 'chiropractic': 0.2165423083, 'rehabilitation_practitioner': 0.3539823009, 'psychologist': 0.2070765661, 'marriage_&_family_therapist': 0.1868131868, 'otolaryngology': 0.1044740129, 'peripheral_vascular_disease': 0.1811724386, 'psychiatry': 0.0807278933, 'nurse_practitioner': 0.1024292764}
# 
# 3.2) The standard deviation of these fractions is 0.1403177353.
# 
# 4.1)
# 
# {'GA': 1.111326632, 'WA': 1.3435720027, 'DE': 0.7742253985, 'DC': 1.1008448679, 'WI': 1.2856167057, 'WV': 0.9508338504, 'HI': 0.4576870296, 'CO': 1.0798288179, 'FL': 1.0540031216, 'WY': 0.7634733555, 'NH': 1.211005896, 'NJ': 0.6015528086, 'NM': 0.8691995683, 'TX': 0.9852625733, 'LA': 1.0217397161, 'NC': 1.4208254553, 'ND': 0.6192260374, 'NE': 0.6214357308, 'TN': 1.3987119042, 'NY': 0.5643903794, 'PA': 0.9916831945, 'RI': 0.5580206257, 'NV': 1.405475954, 'AA': 0, 'VA': 0.8617942113, 'GU': 0.4299820467, 'AE': 1.0559284116, 'VI': 0.4352847471, 'AK': 1.3141289438, 'AL': 0.9563268386, 'AP': 0.65, 'XX': 0.1964285714, 'AR': 0.9519900679, 'VT': 0.7027027027, 'IL': 0.6837681118, 'ZZ': 0.8887515451, 'IN': 1.0290679085, 'IA': 0.6118675366, 'OK': 1.1747665475, 'AZ': 1.139460175, 'CA': 0.8277269932, 'ID': 1.1483248571, 'CT': 0.8146223146, 'ME': 1.2621179179, 'MD': 1.1521115889, 'MA': 0.8635142544, 'OH': 0.9383874293, 'UT': 0.9286944106, 'MO': 1.0003617218, 'MN': 0.7707146268, 'MI': 1.1408633303, 'KS': 0.789162269, 'MT': 0.9356945491, 'MP': 0.2374100719, 'MS': 0.9031742045, 'PR': 0.5322919176, 'SC': 1.1180378933, 'KY': 1.0343620377, 'OR': 1.3600014553, 'SD': 0.6787904645}
# 
# 4.2) The difference between the largest and smallest ratios is 1.4208254553.
# 
# 5.) The Pearson correlation coefficient between these values is -0.240401625808. Value shows negative linear correlation.
# 
# 6.) States which have surprisingly high supply of opioids, conditioned on specialty.
# 
# assistant,_podiatric - MO,  clinical_psychologist - TX,  health_maintenance_organization - PR,  spec/tech,_cardiovascular - MI,  technician - NJ,  surgical_oncology - LA,  hospital_(dmercs_only) - DC,  respiratory_therapist,_certified - CA,  nursing_facility,_other_(dmercs_only) - OH,  psychologist_(billing_independently) - NY,  maxillofacial_surgery - NV,  pharmacy - CA,  respite_care - SC,  denturist - FL,  clinical_medical_laboratory - IA,  plastic_surgery - KS,  military_health_care_provider - VA,  allergy/immunology - NM,  physical_medicine_and_rehabilitation - KY,  preventive_medicine - OK,  homeopath - PR,  hematology - MO,  unknown_physician_specialty_code - FL,  legal_medicine - SC,  ophthalmology - TN,  exclusive_provider_organization - MI,  general_surgery - SC,  chronic_disease_hospital - PR,  preferred_provider_organization - WA,  optician - NJ,  general_acute_care_hospital - MO,  physical_therapist - NY,  speech_language_pathologist - WI,  nephrology - WV,  family_medicine - PA,  medical_oncology - OK,  substance_abuse_rehabilitation_facility - MD,  public_health_welfare_agency - UT,  licensed_vocational_nurse - NY,  social_worker - FL,  student_in_an_organized_health_care_education/training_program - SC,  dental_assistant - PA,  rheumatology - SC,  mass_immunization_roster_biller - MD,  neurology - KY,  cardiac_surgery - RI,  snf_(dmercs_only) - NY,  neuropsychiatry - FL,  surgery - NM,  obstetrics/gynecology - AL,  gastroenterology - MS,  nuclear_medicine - OK,  home_health_aide - NJ,  licensed_practical_nurse - IL,  licensed_clinical_social_worker - CA,  psychiatry_&_neurology - WV,  hospice_and_palliative_care - MO,  specialist - NC,  rehabilitation_agency - MO,  occupational_therapy_assistant - NY,  pediatrics - AZ,  radiation_oncology - WV,  gynecological/oncology - IN,  infectious_disease - FL,  hand_surgery - AZ,  orthopaedic_surgery - WA,  point_of_service - AZ,  pharmacy_technician - PR,  general_practice - VA,  rehabilitation_practitioner - NY,  certified_nurse_midwife - TN,  clinical_neuropsychologist - OH,  pulmonary_disease - GA,  hearing_instrument_specialist - FL,  thoracic_surgery - MN,  military_hospital - CA,  physical_therapy_assistant - FL,  technician/technologist - TX,  radiologic_technologist - NC,  sleep_medicine - KS,  internal_medicine - VA,  thoracic_surgery_(cardiothoracic_vascular_surgery) - NY,  medical_supply_company,_other - CA,  emergency_medicine - ID,  specialist/technologist - CA,  emergency_medical_technician,_paramedic - PR,  interventional_radiology - MO,  independent_medical_examiner - GA,  mechanotherapist - MN,  dental_hygienist - MA,  audiologist_(billing_independently) - PR,  psychoanalyst - CT,  hematology/oncology - WA,  medical_genetics,_ph.d._medical_genetics - PR,  radiology - TX,  urology - MS,  genetic_counselor,_ms - CA,  interventional_cardiology - KY,  multispecialty_clinic/group_practice - MI,  health_educator - PA,  centralized_flu - MI,  community_health_worker - FL,  family_practice - TN,  contractor - NJ,  slide_preparation_facility - DC,  unknown_supplier/provider - ND,  osteopathic_manipulative_medicine - WV,  plastic_and_reconstructive_surgery - MA,  occupational_therapist - VA,  diagnostic_radiology - FL,  geriatric_medicine - MO,  dentist - MA,  clinic/center - OH,  crna - NH,  driver - FL,  specialist/technologist,_other - MD,  cardiology - MD,  sports_medicine - TX,  oral_&_maxillofacial_surgery - GA,  critical_care_(intensivists) - WA,  chiropractic - ID,  case_manager/care_coordinator - PA,  medical_genetics - MD,  pain_management - OK,  addiction_medicine - AZ,  counselor - TX,  emergency_medical_technician,_intermediate - SC,  podiatry - TN,  neurological_surgery - VA,  geriatric_psychiatry - MI,  endocrinology - AR,  oral_surgery_(dentists_only) - ZZ,  nurse's_aide - CO,  dermatology - WA,  neurosurgery - WI,  durable_medical_equipment_&_medical_supplies - FL,  interventional_pain_management - KY,  midwife - FL,  pathology - MD,  obstetrics_&_gynecology - LA,  physician_assistant - NJ,  colorectal_surgery_(formerly_proctology) - KY,  hospitalist - NH,  midwife,_lay - MS,  vascular_surgery - NM,  registered_dietician/nutrition_professional - OH,  behavioral_analyst - FL,  ambulatory_surgical_center - TX,  orthopedic_surgery - OK,  certified_clinical_nurse_specialist - WY,  electrodiagnostic_medicine - DE,  pharmacist - NM,  anesthesiologist_assistants - GA,  massage_therapist - KY,  optometry - LA,  registered_nurse - WY,  anesthesiology - AR,  rehabilitation,_substance_use_disorder_unit - MA,  colon_&_rectal_surgery - NY,  clinical_pharmacology - TN,  acupuncturist - VA,  emergency_medical_technician,_basic - MA,  religious_nonmedical_nursing_personnel - CA,  pediatric_medicine - KY,  physical_medicine_&_rehabilitation - TX,  community/behavioral_health - CA,  cardiac_electrophysiology - KY,  adult_companion - OR,  naturopath - WA,  neuromusculoskeletal_medicine,_sports_medicine - FL,  personal_emergency_response_attendant - VA,  psychologist - PR,  marriage_&_family_therapist - FL,  otolaryngology - SC,  peripheral_vascular_disease - WI,  psychiatry - VT,  nurse_practitioner - UT, 
