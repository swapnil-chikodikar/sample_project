# <!--<div class="mx-auto" style="width: 600px;">-->
#     <!--<div class="card mb-4 border">-->
#         <!--<div class="card-body" align="center">-->
#             <!--<h2 class="card-title">Environment Deployment</h2>-->
#             <!--<h4 class="card-title">VM Creation</h4>-->
#             <!--<br>-->
#
#             <!--<form class="needs-validation" method="POST" novalidate action="/sample_app/deployment/">-->
#                 <!--{% csrf_token %}-->
#                 <!--<div class="form-row">-->
#                     <!--<div class="col-md-4 mb-3">-->
#                         <!--<label for="validationTooltip01">Cluster name</label>-->
#                         <!--<input type="text" class="form-control" id="validationTooltip01" placeholder="Cluster name"-->
#                                <!--name="esx_host" required>-->
#                         <!--<div class="valid-tooltip">-->
#                             <!--Looks good!-->
#                         <!--</div>-->
#                     <!--</div>-->
#                     <!--<div class="col-md-4 mb-3">-->
#                         <!--<label for="validationTooltip02">Data Center name</label>-->
#                         <!--<input type="text" class="form-control" id="validationTooltip02" placeholder="DC name"-->
#                                <!--name="dc_name" required/>-->
#                         <!--<div class="valid-tooltip">-->
#                             <!--Looks good!-->
#                         <!--</div>-->
#                     <!--</div>-->
#                     <!--<div class="col-md-4 mb-3">-->
#                         <!--<label for="validationTooltip03">Data Store name</label>-->
#                         <!--<input type="text" class="form-control" id="validationTooltip03" placeholder="DS name"-->
#                                <!--name="ds_name" required>-->
#                         <!--<div class="valid-tooltip">-->
#                             <!--Looks good!-->
#                         <!--</div>-->
#                     <!--</div>-->
#                 <!--</div>-->
#                 <!--<div class="form-row">-->
#                     <!--<div class="col-md-4 mb-3"><label for="exampleFormControlSelect1">Select Template</label>-->
#                         <!--<select class="form-control" name="temp_name" id="exampleFormControlSelect1" required>-->
#                             <!--<option value="" selected disabled hidden>Choose template</option>-->
#                             <!--<div class="invalid-tooltip">-->
#                                 <!--Please select at least one Template.-->
#                             <!--</div>-->
#                             <!--<option value="AD-win2012-bkp">AD-win2012-bkp</option>-->
#                             <!--<option value="APP-rhel7">APP-rhel7</option>-->
#                             <!--<option value="APP-win12-bkp">APP-win12-bkp</option>-->
#                             <!--<option value="APP-win-latest">APP-win-latest</option>-->
#                             <!--<option value="Auto-win12.bkp">Auto-win12.bkp</option>-->
#                             <!--<option value="Mysql-rhel7-Template">Mysql-rhel7-Template</option>-->
#                             <!--<option value="SQL-win12-bkp">SQL-win12-bkp</option>-->
#                         <!--</select>-->
#                     <!--</div>-->
#                     <!--<div class="col-md-4 mb-3">-->
#                         <!--<label for="validationTooltip04">Start Range</label>-->
#                         <!--<input type="number" min="0" class="form-control" id="validationTooltip04" placeholder="0"-->
#                                <!--name="s_range" required>-->
#                         <!--<div class="invalid-tooltip">-->
#                             <!--Please select at least one VM.-->
#                         <!--</div>-->
#                     <!--</div>-->
#
#                     <!--<div class="col-md-4 mb-3">-->
#                         <!--<label for="validationTooltip05">End Range</label>-->
#                         <!--<input type="number" min="0" class="form-control" id="validationTooltip05" placeholder="0"-->
#                                <!--name="e_range" required>-->
#                         <!--<div class="invalid-tooltip">-->
#                             <!--Please select at least one VM.-->
#                         <!--</div>-->
#                     <!--</div>-->
#                 <!--</div>-->
#                 <!--<div class="col-md-8 mb-3">-->
#                     <!--<label for="validationTooltip06">New VM Name</label>-->
#                     <!--<input type="text" class="form-control" id="validationTooltip06"-->
#                            <!--placeholder="eg. Template_name-test"-->
#                            <!--name="new_vm" required>-->
#                     <!--<div class="invalid-tooltip">-->
#                         <!--Please provide a valid VM Name.-->
#                     <!--</div>-->
#                 <!--</div>-->
#                 <!--<button id="btn" class="btn btn-primary" type="submit">DEPLOY</button>-->
#             <!--</form>-->
#
#         <!--</div>-->
#
#     <!--</div>-->
#
# <!--</div>-->
# <!--<div id="loadpage" hidden-->
#      <!--style="position:relative; left:0px; top:0px; background-color:white; layer-background-color:white; height:100%; width:100%;">-->
#     <!--<p align="center" style="font-size: large;">-->
#         <!--<img src="spinner.gif">-->
#         <!--<B>Loading ... ... Please wait!</B>-->
#     <!--</p>-->
# <!--</div>-->
# <!--<br>-->

# for i in range(3,4):
#     new_name = "name" + "%s" %i
#     print(new_name)
#     onclick = "end_range.min=start_range.value"

dns1 = 10.12
dns2 = 10.14
dns_list = [dns1, dns2]
print(dns_list)