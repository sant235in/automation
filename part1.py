import groovy.json.JsonSlurperimport java.util.Arrays
// def arrayList = ['dev', 'qa', 'qdeva', 'uat']
// println list
def return_list = []def file = "/Users/A200167708/.jenkins/workspace/json-check-pipeline/file.json"def jsonString = new File(file).textdef environmentSpecific = new JsonSlurper().parseText(jsonString)['EnvironmentSpecific']
environmentSpecific.each { env, configurations -> // println "Adding choice: $env" return_list.add("\'$env\'")}
// println "Choices: $return_list"println(return_list.getClass())println return_listdef newlist = Arrays.asList(return_list.toArray())println(newlist.getClass())println newlistreturn return_list
