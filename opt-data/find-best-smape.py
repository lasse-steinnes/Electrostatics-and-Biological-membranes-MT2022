### File to find best SMAPE value from text file ###
import numpy as np

def find_min(infile, threshold, opt_name, all_xi = False, SMAPE = True):
    ## Read off lines to find the lowest SMAPE, and get the interactions parameters
    lines = infile.readlines()
    min_list = [] # an empty list

    if infile.mode == "r":
        if SMAPE is True:
            if all_xi is False:
                min_ind = 180
                max_ind = 195
            else:
                min_ind = 285
                max_ind = 300

        else: # find minimum total R2 value
            if all_xi is False:
                min_ind = 150
                max_ind = 180

            else:
                # if 10
                min_ind = 255
                max_ind = 285

                # if 8
                #min_ind = 226
                #max_ind = 249

        opt_len = int(np.shape(lines)[0])
        i = 1
        num = 0

        if SMAPE is True:
            while i < opt_len:

                val = float(lines[i][min_ind:max_ind])

                if val <= threshold:
                    min_list.append(lines[i])
                    num += 1
                i += 1
        else:
            while i < opt_len:

                val = float(lines[i][min_ind:max_ind])

                if val >= threshold:
                    min_list.append(lines[i])
                    num += 1
                i += 1


    print("\n")
    print("Optimization-type:", opt_name)
    #print("Lowest smape value:", SMAPE_lowest)
    #print("Simulation number:", i_min)
    print("\n")
    print(lines[0])
    print(min_list)
    print("Numbers of optimizations within threshold:", num)
    infile.close()

thresh = 27.7
threshr2 = 0.941
infile = open("opt-data/directed-search/opt_data-GPE-dir.txt", "r") # three x_ij
#find_min(infile, thresh, "opt_data_GPE_dir")
find_min(infile, threshr2, "opt_data-GPE-dir", SMAPE = False)


"""
thresh = 27.45
threshr2 = 0.9415
infile = open("opt-data/directed-search/opt_data_PE_dir.txt", "r") # three x_ij
#find_min(infile, thresh, "opt_data_GPE_dir")
find_min(infile, thresh, "opt_data-PE-dir", SMAPE = True)
"""

"""
#thresh = 5000
threshr2 = 0.91
infile2 = open("opt-data/random-search/opt_data_PE_rand.txt", "r") # all ten x_ij
#find_min(infile2, thresh, "opt_data_GPE_random" ,all_xi = True)
find_min(infile2, threshr2, "opt_data_PE_rand" ,all_xi = True, SMAPE = False) # 10 instead of 12 (what the heck)
"""

"""
thresh = 5000
threshr2 = 0.785
infile2 = open("opt-data/random-search/viable-opt_data-GPE-random.txt", "r") # all ten x_ij
#find_min(infile2, thresh, "opt_data_GPE_random" ,all_xi = True)
find_min(infile2, thresh, "opt_data_GPE_random" ,all_xi = True, SMAPE = True)
"""

### choice among 10 BEST (which makes sense) ###
""" R2
(* BEST overall)

Random:
GPE:
            L,G            L,C            G,P            C,W            P,C            P,W            N,P            N,C            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['   5.3500626460  -2.5596368839   1.9766259620  24.1691452104   3.1346362271 -22.9605639354 -22.6026238538  34.6692947514  -0.4768314698   0.2283550861             40.973109996             2.7711892805             2.6714279381            8140678686600            0.80108393548             4081.8281047\n',
 '   3.3596427433  34.0899470995   4.5229187894  24.4964328726  30.1951231795  -4.7360061941  -1.5322466319  16.0653379029 -10.1307128582   3.5270628493             68.105945844             3.4644168293             3.3762867692            4571436738400            0.78512499518             6785.8551485\n',
 '   8.1375752563  12.7951598729  -0.1799968950  25.0211202180  -1.3883305524 -11.9627286109   6.6278308233  32.2738083853   3.7609630018   6.3714461174             82.526392799             3.8174738221             3.7172342664            7150221538200             0.7864432025             8222.7540671\n',
 '   2.5327994928  16.5831342902  30.4630144830  37.6693031920   7.8159215102   6.3340622095 -24.7510992270  15.9502371220  -5.6730898220 -15.1019471334             70.313091592             3.5727135921             3.4569837361            8566230623600            0.78842309973             7003.2642546\n',
 '  28.5311157280  -3.8110897441   2.6169060791  45.6062280976   6.9936711838   1.2853778996 -29.0607148057  23.6688492856  10.8352481807 -11.6501429509             97.165909056             4.1665323189              4.038727792            4407109758100            0.78572443525             9679.6530045\n',
 '   6.6883746738  29.6175853530  17.0370603696  22.5084492029   8.0489767200  -7.4881656904 -19.7567282654  38.7918027083 -11.2558642567   1.3918096355             57.662236124             3.2257055779             3.1358552624            5451260372800            0.78760934979             5755.9306682\n',
 '  -0.5598684489   6.4935942509  -4.7504882991  17.7352389585  26.4631293981   3.3186738641   1.7867099690  15.5229264133   5.6093726518   6.0737018691              87.68735208             3.8938608566             3.8050071354            6768623322400            0.79518747459             8746.2430721\n',
 '  -0.1968327461  -0.7906314023  31.0553558848  16.2265282684  28.5737800846   2.2019994119 -23.1127361670  30.9899306586   8.5220992100  18.3338737032             100.86738871             4.1900926891             4.0879680067            3065272577300            0.79160738359             10049.774145\n',
 '  11.6971029969   1.8824471391   7.6161428344  24.7030015943  32.2825238512 -20.8205990860 -10.2722434029   4.9639078808 -12.6412808310  -5.7219546664             22.797236861             2.0847061305             2.0112526149            7128993888500             0.8047576545             2279.1760676\n',
 '   7.3815845444  12.1884880456  -0.7926140963  32.2965239228  -4.7147096378  -5.5549178055  -7.8160685736  40.4413263854 -13.3637912549 -13.0588901811             37.121366763             2.6520447212             2.5492930599            7525326590500            0.80390697846             3699.4266196\n']

PE:
            L,G            L,C            G,P            C,W            P,C            P,W            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['   2.3884302481  15.5541542245   2.0785658609  15.6790076273  25.9792257625 -10.3734336831   3.0586668739  11.8991189776        0.550585081922222        0.447721118911111        0.343661466677778         8949928480222.22        0.917424962011111         36.9027985666667\n',
'  -0.3456680691  15.4787018215  23.8857350480  23.7577878668  31.0998228113 -12.9872758227 -10.8417731502  -3.2154332372            0.38375652002            0.35475048064             0.2678507482            7170658353500            0.93442167207             30.379036744\n',
'  -3.1040462570   1.7344719797  -0.1611544804  34.1952512282  24.5889064723 -17.4648177733  -0.8119109503 -11.3109868609             0.5856818202            0.52726056384              0.358774612            5710653924300            0.91110074292             34.817535977\n',
'   4.6195449252  -0.1245681549  22.4379009780  28.4920467906  27.4565301379  -6.5595242317  -1.6899389444   0.4982015815            0.65026965131            0.46829140107            0.33822989671            7387430114800            0.92883972912             33.164340557\n',
'   7.6609918656  16.4268989012  -3.4269622072  37.6416630739  -1.3328671418 -20.8747216814  -0.7681758365 -13.2142052347            0.54703553226            0.48032214612             0.3430905714           10118929121400             0.9158003116             32.242349646\n',
'  -0.7069434423   2.8675394578  17.1756049996  38.4748462422  15.4091224089 -13.0441719160 -13.5147647054 -12.1070312854            0.64400261915            0.51501947533            0.36637527642            8842481425800            0.92463452058             39.205706531\n',
'  16.8790793656   6.3779130901   1.2981190373  30.9990027831  23.0042910023   3.1324659027  -0.2854303501  -5.2623698224            0.68452924064            0.48086271879            0.35480878455           10775945682000            0.92276533716             30.736211307\n',
'   2.2498230070  -0.3661165089  15.6503766934  21.6368286560  24.1217610554   5.2715746587 -13.4165959979  -9.4459798350            0.48484441394            0.47949087679            0.34843840698           22968191813000            0.91289163893             31.277255874\n',
'  -0.3918275263   9.4182049709  29.6113522804  24.7383004447  15.4732536751  -0.2888207188  -8.9155779135  -7.6220153683            0.54054877421            0.47937184169            0.35010558201           20465118961000            0.91428398281             29.369714573\n',
'  21.3393363261  21.1907243887   0.7227736237  22.7159811734  22.2384194410 -17.2537708483 -10.1636608612   5.1121749503            0.48181059849            0.40727809598            0.30844771882            7641495942400             0.9232585376             31.956810867\n']


Directional:
GPE: (11 best)
            C,W            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['  25.2835315265 -11.7136756992  -9.1720043113            0.42131455213            0.36877325553            0.27464466537            7901971687800               0.94104658             27.702594577\n',
'  24.5909180218 -12.4842257075  -8.9427576050            0.41106585467            0.36520475521            0.27262242258            8127484245800             0.9413168553             27.996513234\n',
'  25.4150330827 -12.5410994950  -9.7907859177            0.41536416229            0.36679451341            0.27228982728            7917413762000            0.94175319702              28.02238591\n',
'  25.3815392944 -11.6743046172  -9.4199792512            0.41961606467            0.36843786312            0.27429600663            7965488144600            0.94119943833             27.724508599\n',
'  25.3826245116 -11.6733903580  -9.4220188460            0.41949826811            0.36806028645              0.274284799            7922075520300            0.94105407662             27.880794261\n',
'  25.3942351592 -11.6641037855  -9.4441814195            0.42020054481            0.36867954092            0.27449494431            8026091002600            0.94109028452             27.771504151\n',
'  25.4817170265 -11.6011221257  -9.6016468424            0.41841335831            0.36776186801            0.27412039352            8019389725000             0.9411102334             27.827672641\n',
'  25.2480050363 -11.7812241960  -9.1476483130            0.42217723954            0.36924219234            0.27482892889            7887986412700            0.94117605212             27.685281102\n',
'  25.2478528818 -11.7812805775  -9.1471685343            0.42167964003            0.36910380775            0.27472718502            7926154558900            0.94118688538             27.630478539\n',
'  25.5141643409 -12.6047266837  -9.1949182736            0.42700370651            0.37168815571             0.2742108403            7568364608900            0.94192734495             28.812061828\n',
*'  25.2494029620 -11.4724110646  -9.2426418066            0.42031109951            0.36880736966            0.27528346398            7999285892400            0.94104225226             27.510442693\n']


PE: (17 best)
            C,W            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['  25.3500626460 -11.2596368839  -8.5233740380            0.45049475691            0.38184182004            0.28371103139            8976506977000            0.94193316176             28.473731133\n',
'  25.2367459917 -11.5823718399  -8.5567582033            0.44773806705            0.38062873669            0.28279473326            9044393832500             0.9425066403             28.707064179\n',
'  25.6445840554 -11.2302301307  -8.9086836028            0.45035248503            0.38195553428            0.28359195802            8959316743200            0.94188507671              28.50261702\n',
'  25.0677141078 -11.1019146024  -8.0840372906            0.45104705511            0.38162565753            0.28393153028            9114611566900            0.94166348427             28.319246347\n',
'  25.7520496678 -11.2096828212  -9.1118818425            0.44787431714            0.38117048001            0.28310510878            9183663862000            0.94183495491             28.408987103\n',
'  25.3172965723 -10.9996296717  -8.4680881895            0.44933583165             0.3810242394            0.28323761468            9106453489700            0.94175444084             28.105086964\n',
'  25.3170070502 -10.9865987551  -8.4768170296            0.44987416121            0.38148471628            0.28385880965            9198814576200            0.94164349397             28.532268227\n',
'  28.2889845232 -13.7000000000 -15.5000000000            0.40184067152            0.37283575201            0.27412903665            9859036096100            0.94389957672             28.995362921\n',
'  21.8469910278 -13.5704602515  -7.3206643178            0.39740416351            0.36786199577            0.27639336605           10172247981400            0.94180096912             28.092463455\n',
'  21.7372310746 -13.7000000000  -5.1838177480            0.42704081958            0.37640987051            0.28143208486            9132675880400            0.94236661331             29.371918038\n', '
26.7354537615 -13.6417295975 -13.0500558025            0.40716764832            0.37085837158            0.27455171091            9695874555600            0.94415900594             28.691994242\n', '
27.0139510199 -13.7000000000 -12.7717164250            0.41667911982            0.37264564499            0.27488911355            9390238026600            0.94455808744             29.563090908\n', '
 22.7763479908 -13.6368794346  -8.6675103167            0.39476259259            0.36647594758            0.27493287373           10289957378000             0.9424318715             27.751205758\n',
* '  22.6356573936 -13.7000000000  -9.0493514103            0.38785092139            0.36724761007            0.27531315518           10526832975000            0.94159853882             27.519889552\n',*
  '  22.8078278861 -13.7000000000  -9.0878549075             0.3911120997             0.3677458233            0.27578508957           10472057313000            0.94175104863             27.843315244\n',
  '  22.8088343452 -13.7000000000  -9.0884082320            0.38978532534            0.36703255952            0.27530956384           10461568356000            0.94194121752             27.904375911\n',
  '  23.1919904926 -13.7000000000  -9.3160546998            0.39444516675            0.36742485071            0.27528512541           10215660606800            0.94243390731             27.937129648\n']

"""

"""
Best by smape

Random
PE


GPE
            L,G            L,C            G,P            C,W            P,C            P,W            N,P            N,C            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['   5.3500626460  -2.5596368839   1.9766259620  24.1691452104   3.1346362271 -22.9605639354 -22.6026238538  34.6692947514  -0.4768314698   0.2283550861             40.973109996             2.7711892805             2.6714279381            8140678686600            0.80108393548             4081.8281047\n',
'  -0.3456680691  15.4787018215  23.8857350480  23.7577878668  31.0998228113 -12.9872758227 -27.1417731502  13.7845667628  -7.2006457321 -11.5230025703             45.788998809              3.293646057             3.1118715494          102295043649000            0.45379977118             4540.5206102\n', '
8.8649351685  -2.1424737753  12.1390837930  35.0318260868   0.4845615077   2.5708174387 -22.3124001442  34.6783666692 -11.3920688170  -8.2557966871             42.056066892             2.9140558059             2.7568681064           19039952851000            0.76900469645             4178.1429285\n',
'  11.6971029969   1.8824471391   7.6161428344  24.7030015943  32.2825238512 -20.8205990860 -10.2722434029   4.9639078808 -12.6412808310  -5.7219546664             22.797236861             2.0847061305             2.0112526149            7128993888500             0.8047576545             2279.1760676\n',
'   7.3815845444  12.1884880456  -0.7926140963  32.2965239228  -4.7147096378  -5.5549178055  -7.8160685736  40.4413263854 -13.3637912549 -13.0588901811             37.121366763             2.6520447212             2.5492930599            7525326590500            0.80390697846             3699.4266196\n',
'  -2.7237290938   7.7391505547  29.8267472433  18.4962886245  10.1996036942 -11.5342997936 -17.7773647630  18.5507014823 -10.1911764683  18.9535867829             41.041379469             2.8817487459             2.7363969119            4786210603100            0.76421265102             4072.3693043\n']

Directional:
PE
       C,W            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

*['  24.9012787440 -10.2334474172  -8.4428815382            0.44379318761            0.38317870836            0.28653329247            9655666890100            0.93988658485             27.364646163\n',
'  26.6784365023  -5.0480041261  -5.9378462812            0.52321376936             0.4106976649            0.30495179266            8539758496000            0.93459711214             27.428747191\n',
'  26.6791988091  -5.1232963009  -6.0250005302            0.52092093255            0.41023939404            0.30475509176            8568020405500            0.93465584622             27.439157601\n',
'  27.3441389810  -2.3983473124  -4.5430236753            0.55931929923            0.42618058807            0.31572161278            8032500920300            0.93139862391             27.446875131\n',
'  27.4219520573  -2.2846810259  -4.4492555575            0.56171096589            0.42716552337            0.31679928355            7934021276100            0.93082465695             27.389174438\n',
'  27.2341436921  -2.5306241102  -4.4887513666            0.55579178117            0.42449900984            0.31493007223            8060180110200            0.93163369986             27.442731751\n',
'  27.4105705781  -2.3747261500  -4.5085432480            0.56150539845            0.42669158071             0.3160985614            7894104970400            0.93120489866             27.416998945\n',
'  27.3325315587  -2.3384108711  -4.1082477916             0.5661549517             0.4271552365            0.31608157916            7898184009100            0.93123665816             27.449289989\n',
'  27.3228711438  -2.3607488351  -4.1207607013            0.56577666481            0.42729179744            0.31649353212            7922366880300            0.93107461845             27.415074763\n']


GPE
            C,W            G,C            G,W                      MSE                     RMSE                      MAE                     MAPE                       R2                    SMAPE

['  25.2827045282 -11.7110339728  -9.1642003153            0.42184627302             0.3688978543            0.27470795238            8005695809900            0.94093197381             27.564734501\n',
'  25.2480050363 -11.7812241960  -9.1476483130            0.42217723954            0.36924219234            0.27482892889            7887986412700            0.94117605212             27.685281102\n',
'  25.2478528818 -11.7812805775  -9.1471685343            0.42167964003            0.36910380775            0.27472718502            7926154558900            0.94118688538             27.630478539\n',
'  25.6741594208 -11.2386478217  -9.6109781643            0.42233786107            0.37017521466            0.27578891962            7983552458000            0.94068100852             27.662462343\n',
'  24.8532401015 -11.6955636465  -9.4197138549            0.40698437146            0.36622083023            0.27437275012            8315994097200            0.94017651672             27.647628565\n',
'  25.2481094911 -11.4601778182  -9.2341891528            0.41965955314            0.36916096088            0.27567252474            8064841868500            0.94045814605             27.414678226\n',
'  25.2466467056 -11.4395653426  -9.2206951647            0.42041192699             0.3693286126            0.27568786486            8025508282700            0.94068194543             27.663242054\n',
'  25.2494029620 -11.4724110646  -9.2426418066            0.42031109951            0.36880736966            0.27528346398            7999285892400            0.94104225226             27.510442693\n',
'  25.2492210754 -11.4723337999  -9.2424559649            0.41968338411            0.36868730637            0.27498289422            7971023982600            0.94085292083             27.454175914\n',
'  25.2494038736 -11.4703909715  -9.2414822880            0.41889342487            0.36851461974            0.27504213663            8109419932400            0.94077882083             27.646031775\n',
*'  25.2640220959 -11.4824667804  -9.2726067829            0.41844380914             0.3682559891            0.27516520774            8134768243100            0.94049856502             27.399427588\n']

"""
