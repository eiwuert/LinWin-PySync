Search.setIndex({envversion:49,filenames:["README","deb_dist/localboxsync-1.6.0b1/README","docs/_apidoc/modules","docs/_apidoc/sync","docs/_apidoc/sync.controllers","docs/_apidoc/sync.gui","docs/_apidoc/sync.models","docs/_apidoc/sync.resources","docs/source/contributions","docs/source/includeme","docs/source/nextsteps","docs/source/specification","docs/source/usermanual","index"],objects:{"":{sync:[3,0,0,"-"]},"sync.auth":{AlreadyAuthenticatedError:[3,1,1,""],AuthenticationError:[3,1,1,""],Authenticator:[3,2,1,""],generate_client_id:[3,4,1,""],generate_client_secret:[3,4,1,""]},"sync.auth.Authenticator":{authenticate_with_client_secret:[3,3,1,""],authenticate_with_password:[3,3,1,""],get_authorization_header:[3,3,1,""],has_client_credentials:[3,3,1,""],init_authenticate:[3,3,1,""],is_authenticated:[3,3,1,""],load_client_data:[3,3,1,""],password_authentication:[3,3,1,""],save_client_data:[3,3,1,""]},"sync.controllers":{account_ctrl:[4,0,0,"-"],localbox_ctrl:[4,0,0,"-"],login_ctrl:[4,0,0,"-"],preferences_ctrl:[4,0,0,"-"]},"sync.controllers.account_ctrl":{AccountController:[4,2,1,""],Preferences:[4,2,1,""]},"sync.controllers.account_ctrl.AccountController":{"delete":[4,3,1,""],add:[4,3,1,""],load:[4,3,1,""],save:[4,3,1,""]},"sync.controllers.localbox_ctrl":{SyncItem:[4,2,1,""],SyncsController:[4,2,1,""]},"sync.controllers.localbox_ctrl.SyncItem":{direction:[4,5,1,""],label:[4,5,1,""],path:[4,5,1,""],url:[4,5,1,""],user:[4,5,1,""]},"sync.controllers.localbox_ctrl.SyncsController":{"delete":[4,3,1,""],add:[4,3,1,""],get:[4,3,1,""],list:[4,5,1,""],load:[4,3,1,""],save:[4,3,1,""]},"sync.controllers.login_ctrl":{InvalidPassphraseError:[4,1,1,""],LoginController:[4,2,1,""]},"sync.controllers.login_ctrl.LoginController":{get_passphrase:[4,3,1,""],logged_in:[4,5,1,""],store_keys:[4,3,1,""],store_passphrase:[4,3,1,""]},"sync.controllers.preferences_ctrl":{Preferences:[4,2,1,""],PreferencesController:[4,2,1,""]},"sync.controllers.preferences_ctrl.PreferencesController":{get_language_abbr:[4,3,1,""],load:[4,3,1,""],prefs:[4,5,1,""],save:[4,3,1,""]},"sync.database":{DatabaseError:[3,1,1,""],database_execute:[3,4,1,""],get_sql_log_dict:[3,4,1,""],mysql_execute:[3,4,1,""],sqlite_execute:[3,4,1,""],warning_no_database_section:[3,4,1,""]},"sync.gpg":{gpg:[3,2,1,""]},"sync.gpg.gpg":{add_keypair:[3,3,1,""],add_pkcs7_padding:[3,6,1,""],decrypt:[3,3,1,""],encrypt:[3,3,1,""],generate:[3,3,1,""],get_key:[3,3,1,""],has_key:[3,3,1,""],is_passphrase_valid:[3,3,1,""],remove_pkcs7_padding:[3,6,1,""]},"sync.gui":{gui_utils:[5,0,0,"-"],gui_wx:[5,0,0,"-"],taskbar:[5,0,0,"-"],wizard:[5,0,0,"-"]},"sync.gui.gui_utils":{ask_passphrase:[5,4,1,""],iconpath:[5,4,1,""],is_valid_input:[5,4,1,""],show_error_dialog:[5,4,1,""]},"sync.gui.gui_wx":{AccountPanel:[5,2,1,""],BottomPanel:[5,2,1,""],FirstLoginPanel:[5,2,1,""],Gui:[5,2,1,""],LocalboxListCtrl:[5,2,1,""],LoginDialog:[5,2,1,""],LoginPanel:[5,2,1,""],PasshphrasePanel:[5,2,1,""],PassphraseDialog:[5,2,1,""],PreferencesPanel:[5,2,1,""],SyncsPanel:[5,2,1,""]},"sync.gui.gui_wx.BottomPanel":{ApplyOnClick:[5,3,1,""],CloseOnClick:[5,3,1,""],OnClickOk:[5,3,1,""]},"sync.gui.gui_wx.FirstLoginPanel":{ctrl:[5,5,1,""]},"sync.gui.gui_wx.Gui":{InitUI:[5,3,1,""],OnQuit:[5,3,1,""],OnToolbarLocalboxesClick:[5,3,1,""],add_toolbar:[5,3,1,""],hide_before_login:[5,3,1,""],on_close:[5,3,1,""],on_successful_login:[5,3,1,""],show_first_panels:[5,3,1,""]},"sync.gui.gui_wx.LocalboxListCtrl":{"delete":[5,3,1,""],add:[5,3,1,""],populate_list:[5,3,1,""],save:[5,3,1,""]},"sync.gui.gui_wx.LoginPanel":{get_password:[5,3,1,""],get_username:[5,3,1,""]},"sync.gui.gui_wx.PasshphrasePanel":{OnClickClose:[5,3,1,""],OnClickOk:[5,3,1,""]},"sync.gui.gui_wx.PassphraseDialog":{InitUI:[5,3,1,""],OnClickClose:[5,3,1,""],show:[5,6,1,""]},"sync.gui.gui_wx.PreferencesPanel":{OnChoice:[5,3,1,""]},"sync.gui.gui_wx.SyncsPanel":{delete_localbox:[5,3,1,""],newSyncDialog:[5,3,1,""]},"sync.gui.taskbar":{LocalBoxIcon:[5,2,1,""],PassphraseHandler:[5,2,1,""],passphrase_server:[5,4,1,""],taskbarmain:[5,4,1,""]},"sync.gui.taskbar.LocalBoxIcon":{OnTaskBarActivate:[5,3,1,""],OnTaskBarClick:[5,3,1,""],OnTaskBarClose:[5,3,1,""],TBMENU_CHANGE:[5,5,1,""],TBMENU_CLOSE:[5,5,1,""],TBMENU_DELETE_DECRYPTED:[5,5,1,""],TBMENU_GUI:[5,5,1,""],TBMENU_REMOVE:[5,5,1,""],TBMENU_RESTORE:[5,5,1,""],TBMENU_STOP:[5,5,1,""],TBMENU_SYNC2:[5,5,1,""],TBMENU_SYNC:[5,5,1,""],TBMENU_VERSION:[5,5,1,""],create_popup_menu:[5,3,1,""],delete_decrypted:[5,3,1,""],icon_path:[5,5,1,""],start_gui:[5,3,1,""],start_sync:[5,3,1,""],stop_sync:[5,3,1,""]},"sync.gui.taskbar.PassphraseHandler":{do_GET:[5,3,1,""],get_label:[5,3,1,""]},"sync.gui.wizard":{LoginWizardPage:[5,2,1,""],NewSyncInputsWizardPage:[5,2,1,""],NewSyncWizard:[5,2,1,""],PassphraseWizardPage:[5,2,1,""]},"sync.gui.wizard.LoginWizardPage":{call_password_authentication:[5,3,1,""],password:[5,5,1,""],should_login:[5,3,1,""],username:[5,5,1,""]},"sync.gui.wizard.NewSyncInputsWizardPage":{is_authenticated:[5,3,1,""],label:[5,5,1,""],path:[5,5,1,""],select_localbox_dir:[5,3,1,""],url:[5,5,1,""],validate_new_sync_inputs:[5,3,1,""]},"sync.gui.wizard.PassphraseWizardPage":{add_new_sync_item:[5,3,1,""],passphrase:[5,5,1,""],setup_passphrase_panel:[5,3,1,""],store_keys:[5,3,1,""]},"sync.language":{set_language:[3,4,1,""]},"sync.localbox":{InvalidLocalboxError:[3,1,1,""],LocalBox:[3,2,1,""],NoKeysFoundError:[3,1,1,""],create_key_and_iv:[3,4,1,""],getChecksum:[3,4,1,""],get_aes_key:[3,4,1,""]},"sync.localbox.LocalBox":{"delete":[3,3,1,""],authenticator:[3,5,1,""],call_keys:[3,3,1,""],call_user:[3,3,1,""],create_directory:[3,3,1,""],decode_file:[3,3,1,""],encode_file:[3,3,1,""],get_all_users:[3,3,1,""],get_authentication_url:[3,3,1,""],get_file:[3,3,1,""],get_keys_path:[3,6,1,""],get_keys_path_v2:[3,6,1,""],get_meta:[3,3,1,""],is_valid_url:[3,3,1,""],save_key:[3,3,1,""],upload_file:[3,3,1,""]},"sync.metavfs":{MetaVFS:[3,2,1,""],normalize_path:[3,4,1,""]},"sync.metavfs.MetaVFS":{add_child:[3,3,1,""],add_paths:[3,3,1,""],contains_directory:[3,3,1,""],debug_print:[3,3,1,""],gen:[3,3,1,""],get_entry:[3,3,1,""],get_files:[3,3,1,""],get_paths:[3,3,1,""],load:[3,3,1,""],newest:[3,6,1,""],save:[3,3,1,""],yield_directories:[3,3,1,""],yield_files:[3,3,1,""]},"sync.models":{label_model:[6,0,0,"-"]},"sync.models.label_model":{delete_client_data:[6,4,1,""]},"sync.syncer":{MainSyncer:[3,2,1,""],StopSyncException:[3,1,1,""],SyncRunner:[3,2,1,""],Syncer:[3,2,1,""],get_syncers:[3,4,1,""]},"sync.syncer.MainSyncer":{is_running:[3,3,1,""],keep_running:[3,5,1,""],remove_runner:[3,3,1,""],run:[3,3,1,""],stop:[3,3,1,""],sync:[3,3,1,""],thread_pool:[3,5,1,""],waitevent:[3,5,1,""]},"sync.syncer.SyncRunner":{name:[3,5,1,""],run:[3,3,1,""],stop_event:[3,5,1,""]},"sync.syncer.Syncer":{"delete":[3,3,1,""],download:[3,3,1,""],get_file_path:[3,3,1,""],mkdir:[3,3,1,""],populate_filepath_metadata:[3,3,1,""],populate_localbox_metadata:[3,3,1,""],stop_event:[3,5,1,""],syncsync:[3,3,1,""]},"sync.wizard":{ConfigError:[3,1,1,""],Errorwindow:[3,2,1,""],Wizard:[3,2,1,""]},"sync.wizard.Errorwindow":{close:[3,3,1,""]},"sync.wizard.Wizard":{clear:[3,3,1,""],endwizard:[3,3,1,""],exit_button:[3,3,1,""],get_file:[3,3,1,""],next_1:[3,3,1,""],next_2:[3,3,1,""],next_3:[3,3,1,""],next_4:[3,3,1,""],save:[3,3,1,""],translate:[3,3,1,""],validate_server:[3,3,1,""],window1:[3,3,1,""],window2:[3,3,1,""],window3:[3,3,1,""]},sync:{auth:[3,0,0,"-"],controllers:[4,0,0,"-"],database:[3,0,0,"-"],defaults:[3,0,0,"-"],gpg:[3,0,0,"-"],gui:[5,0,0,"-"],language:[3,0,0,"-"],localbox:[3,0,0,"-"],metavfs:[3,0,0,"-"],models:[6,0,0,"-"],remove_decrypted_files:[3,4,1,""],resources:[7,0,0,"-"],syncer:[3,0,0,"-"],wizard:[3,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","exception","Python exception"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","function","Python function"],"5":["py","attribute","Python attribute"],"6":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:exception","2":"py:class","3":"py:method","4":"py:function","5":"py:attribute","6":"py:staticmethod"},terms:{"2ek":8,"byte":3,"case":8,"class":[3,4,5],"default":[],"final":12,"function":[3,5],"new":[],"public":3,"return":[3,4,5],"static":[3,5],"switch":8,"true":[3,4],"try":[4,12],_control:5,_window:5,abbrevi:4,abl:[10,12],abrevi:4,access:12,account:12,account_ctrl:[],accountcontrol:4,accountpanel:5,add:[3,4,5,8,12],add_child:3,add_keypair:3,add_new_sync_item:5,add_path:3,add_pkcs7_pad:3,add_toolbar:5,address:12,after:[8,12],again:8,against:3,agree:12,algorithm:3,alice:10,all:[3,11,12],allow:[0,1,9],alreadi:[3,12],alreadyauthenticatederror:3,also:[3,12],among:10,ani:[11,12],answer:12,applic:[],applicat:[11,12],apply:5,applyonclick:5,appropri:8,apt:8,arg:3,argument:3,armor:3,ask:[11,12],ask_passphras:5,audit:[0,1,9],auth:[],authent:[0,1,3,9],authenticate_with_client_secret:3,authenticate_with_password:3,authentication_url:3,authenticationerror:3,author:3,avail:[0,1,3,9],backend:[3,12],base:[3,4,5],basehttprequesthandl:5,basehttpserv:5,becaus:11,been:3,behav:5,belong:3,between:[3,5],binari:3,binary_path:3,bit:3,both:[0,1,9],bottompanel:5,box:12,branch:8,bridg:5,bug:8,bugfix:8,button:[5,12],call:[3,5,8],call_kei:3,call_password_authent:5,call_us:3,can:12,cancel:5,care:5,caus:8,certain:3,charact:12,check:3,checkout:8,child:3,children:3,choic:8,choos:[8,12],chr:3,clean:8,clear:3,click:[5,12],client_address:5,clone:8,close:[3,12],closeonclick:5,cloud:[0,1,9],code:[0,1,3,8,9],com:[8,12],command:3,compil:8,complet:[0,1,9,12],complex:12,compon:5,comput:12,confidenti:[0,1,9],configerror:3,configpars:3,configur:[0,1,3,5,9,12],constant:[0,1,9],contain:[3,5],contains_directori:3,contempl:8,content:[],control:[],cool:8,creat:[],create_directori:3,create_key_and_iv:3,create_popup_menu:5,credenti:[3,12],ctrl:5,custom:[3,5,11],daler:8,data:[0,1,3,9],databas:[],database_execut:3,databaseerror:3,debug:3,debug_print:3,decod:3,decode_fil:3,decrypt:[3,11,12],delet:[3,4,5,11,12],delete_client_data:6,delete_decrypt:5,delete_localbox:5,depend:12,descript:12,desktop:[0,1,9,11,12],destroi:5,detail:12,develop:[],devic:12,dialog:5,dictionari:3,differ:12,differenti:3,dir:8,direct:[3,4],directli:12,directori:[3,12],disk:11,displai:8,do_get:5,doc:8,doe:4,don:12,done:[3,12],each:12,edit:11,encod:3,encode_fil:3,encrypt:[0,1,3,9,11,12],endwizard:3,entri:3,error:3,errorwindow:3,etc:[3,11,12],eupl:12,event:[3,5],eventu:11,evt_right_down:5,except:[3,4],exception:[3,4],execut:[3,12],exist:4,exit:11,exit_button:3,extract:[],fail:3,fals:[3,4,5],fdx:8,featur:[8,10],feel:12,file:[],file_root_path:3,filenam:3,filepath:3,filesystem:3,fingerprint:3,finish:12,first:[],firstloginpanel:5,flow:8,folder:12,folder_path:3,forc:12,found:12,frame:[3,5],free:12,friendli:[0,1,9],from:[3,4,5,8,11],fs_path:3,ftp:[0,1,9],gen:3,gener:3,generate_client_id:3,generate_client_secret:3,get:[3,4,5,8,12],get_aes_kei:3,get_all_us:3,get_authentication_url:3,get_authorization_head:3,get_entri:3,get_fil:3,get_file_path:3,get_kei:3,get_keys_path:3,get_keys_path_v2:3,get_label:5,get_language_abbr:4,get_meta:3,get_passphras:4,get_password:5,get_path:3,get_sql_log_dict:3,get_sync:3,get_usernam:5,getchecksum:3,gettext:4,git:8,github:[0,1,8,9],give:11,given:3,gnupg:3,goe:12,gpg:[],graphic:5,group:3,gui:[],gui_util:[],gui_wx:[],guidelin:12,has_client_credenti:3,has_kei:3,hash:3,have:11,head:8,header:3,here:[0,1,9,10,12],hide_before_login:5,highest:3,hold:[0,1,9],home:3,host:3,hour:12,how:[5,8,12],html:8,http:[0,1,4,8,9,12],icon:[5,12],icon_path:5,iconpath:5,identifi:[3,12],imag:3,implement:3,includ:[3,10],includem:8,index:[4,8,13],init_authent:3,initi:3,initui:5,input:12,insid:12,instal:[8,11,12],install:[8,12],instanc:3,interfac:[5,12],invalid:3,invalidlocalboxerror:3,invalidpassphraseerror:4,is_authent:[3,5],is_dir:3,is_passphrase_valid:3,is_run:3,is_valid_input:5,is_valid_url:3,issue_number:8,item:[4,5],iter:3,itself:5,john:10,jpg:3,just:[5,12],keep:11,keep_run:3,kei:[3,8],keypair:3,know:12,knowledg:8,kwarg:3,label:[3,4,5,6,12],label_model:[],lang:3,languag:[],languages:8,latest:[0,1,9],lazy_load:4,let:8,librari:3,like:[3,5],link:12,linwin:8,list:[3,4,5,10,11,12],listctrl:5,ljust:3,load:[3,4],load_client_data:3,loauth:[0,1,3,9],local:[3,12],localbox_cli:[3,4,5],localbox_ctrl:[],localbox_inst:3,localbox_path:3,localboxicon:5,localboxinstal:12,localboxlistctrl:5,localboxsync:12,localhost:4,locat:[3,8],log:3,logged_in:4,login_ctrl:[],logincontrol:4,logindialog:5,loginpanel:5,loginwizardpag:5,look:12,loxbox15:[0,1,9],loxgui:8,machin:[0,1,9],mai:3,mail:12,main:[5,12],main_syncing_thread:5,mainsync:3,make:[3,8],manag:[3,5],match:8,memori:4,menu:[5,12],messag:[3,5,8,12],meta:3,metavf:[],metavfs:3,metavfs_entri:3,method:5,metvf:3,mime:[11,12],mimeapp:[11,12],mkdir:[3,8],mode:[11,12],model:[],modif:3,modifi:3,modified_at:3,modul:[],modulemanag:[],monitor:12,more:[8,12],must:12,mysql:3,mysql_execut:3,name:[3,8],necessari:11,need:[3,5,8],newest:3,newsyncdialog:5,newsyncinputswizardpag:5,newsyncwizard:5,next_1:3,next_2:3,next_3:3,next_4:3,node:3,nokeysfounderror:3,none:[3,4,5],normalize_path:3,noth:5,now:[8,12],number:8,oauth2:[0,1,9],object:[3,4],occur:3,on_clos:5,on_successful_login:5,onc:12,once:11,onchoic:5,onclickclos:5,onclickok:5,one:3,onli:12,onquit:5,ontaskbaractiv:5,ontaskbarclick:5,ontaskbarclos:5,ontoolbarlocalboxesclick:5,open:[0,1,8,9,11,12],oper:11,option:[11,12],order:11,org:[0,1,9,12],origin:12,other:[3,12],other_label:4,otherwis:3,own:12,owner:3,packag:[],pad:3,page:[0,1,8,9,13],panel:5,param:[3,4],paramet:[3,4],parent:[3,5],part:3,partial:3,passhphrasepanel:5,passphras:[3,4,5,11,12],passphrase_serv:5,passphrasedialog:5,passphrasehandl:5,passphrasewizardpag:5,password:[3,5],password_authent:3,path:[3,4,5,12],paul:10,penguinformula:12,per:3,period:12,pkcs:3,place:12,poedit:8,populate_filepath_metadata:3,populate_list:5,populate_localbox_metadata:3,popup:5,possibl:12,pot:8,pref:4,prefer:4,preferences_ctrl:[],preferencescontrol:4,preferencespanel:5,present:3,previou:8,pring:3,prior:12,privaci:[0,1,9],privat:3,private_kei:3,privkei:4,problem:3,process:12,program:12,progress:12,proper:3,provid:[0,1,9,12],pubkei:4,public_kei:3,push:12,pycrypto:12,pysync:8,read:5,readi:[5,8],real:5,reboot:12,receiv:[3,4],recommend:12,ref:8,refer:8,regist:11,rel:3,releas:10,remot:[4,12],remov:3,remove_decrypted_fil:3,remove_pkcs7_pad:3,remove_runn:3,replac:[3,8],repo:8,repres:3,request:5,requir:5,resourc:[],respons:3,rest:5,restart:8,result:3,right:[3,12],run:[3,5,12],same:12,santo:12,save:[3,4,5,8],save_client_data:3,save_kei:3,scenario:8,search:13,secret:3,section:11,secur:[],see:12,select:12,select_localbox_dir:5,send:12,send_data:3,serv:12,server:[0,1,3,5,9,11,12],server_url:3,set:[3,11],set_languag:3,setup:12,setup_passphrase_panel:5,should:[3,8,12],should_creat:3,should_login:5,show:5,show_error_dialog:5,show_first_panel:5,signifi:3,signum:3,singl:3,site:[3,5],siteslist:3,softwar:[0,1,9,12],solut:[0,1,9],solv:8,some_cont:3,some_fold:3,somehow:11,sourc:[0,1,9],special:12,sphinxdoc:8,sql:3,sqlite:3,sqlite_execut:3,standalon:5,start:[],start_gui:5,start_sync:5,statement:3,stop:[3,12],stop_ev:3,stop_sync:5,stopsyncexcept:3,store:[0,1,9,11,12],store_kei:[4,5],store_passphras:4,string:[3,8],stronger:3,structur:3,submodul:[],subpackag:[],substitut:3,sudo:[8,11,12],sure:3,symbol:8,sync_list_ctrl:5,syncer:[],synchron:[0,1,3,9,12],syncitem:4,syncrunn:3,syncscontrol:4,syncspanel:5,syncsync:3,system:[3,5,11,12],take:5,target:3,taskbar:[],taskbaricon:5,taskbarmain:5,tbmenu_change:5,tbmenu_close:5,tbmenu_delete_decrypted:5,tbmenu_gui:5,tbmenu_remove:5,tbmenu_restore:5,tbmenu_stop:5,tbmenu_sync2:5,tbmenu_sync:5,tbmenu_version:5,tell:5,test:[8,12],text:8,than:12,thei:[11,12],them:[8,10,11,12],thi:[0,1,3,5,9,11,12],those:[0,1,9],thread:3,thread_pool:3,three:3,time:[3,11,12],titl:5,tkinter:3,todo:[],topwindow:3,track:11,trai:12,translat:[],translatefil:8,tupl:3,two:3,type:[11,12],understood:11,unencrypt:12,uninstal:12,unreach:3,updat:8,upload:[3,12],upload_fil:3,upon:11,upper:8,url:[3,4,5,12],use:12,usernam:[3,5],using:12,usr:[11,12],validate_new_sync_input:5,validate_serv:3,valu:[3,5,8],variabl:3,verbos:3,version:[],via:4,virtual:3,wait:12,waitev:3,want:[5,8,10,11],warning_no_database_sect:3,well:12,what:10,when:[3,5,11,12],where:8,whether:3,whose:12,widget:5,wilson:12,window1:3,window2:3,window3:3,window:5,wish:12,within:[0,1,9],without:[3,8],wizard:[],wizardpagesimpl:5,wrap:3,wx_event:5,wxpython:12,wxwidget:5,xdg:[11,12],xml:[11,12],xxx:12,yep:12,yield_directori:3,yield_fil:3,you:[0,1,5,9,12],your:[],yourlocalbox:[0,1,9,12]},titles:["Localbox Sync Client","Localbox Sync Client","sync","sync package","sync.controllers package","sync.gui package","sync.models package","sync.resources package","Contributions","Localbox Sync Client","Next Steps","Specification","User Manual","Welcome to LoxPySync&#8217;s documentation!"],titleterms:{"default":3,"new":8,account_ctrl:4,adding:8,applic:8,auth:3,client:[0,1,9,11],content:[3,4,5,6,7],contribut:8,control:4,creat:[8,12],databas:3,develop:8,document:[0,1,8,9,13],download:[0,1,9],encryption:11,explane:12,extens:11,file:[10,12],first:12,gpg:3,gui:[3,5],gui_util:5,gui_wx:5,indice:13,installat:12,label_model:6,languag:3,linux:11,localbox:[0,1,3,9,12],localbox_ctrl:4,login_ctrl:4,lox:11,loxpysync:13,manual:[0,1,9,12],metavf:3,model:6,modul:[3,4,5,6,7],next:10,packag:[3,4,5,6,7],preferences_ctrl:4,project:[0,1,9],relat:[0,1,9],resourc:7,secur:12,share:10,side:11,specif:11,start:8,step:10,submodul:[3,4,5,6],subpackag:[3,7],sync:[0,1,2,3,4,5,6,7,9,12],syncer:3,tabl:13,taskbar:5,translat:8,ubuntu:12,update:8,user:[0,1,9,12],version:3,welcom:13,why:[0,1,9],window:12,wizard:[3,5],your:12}})