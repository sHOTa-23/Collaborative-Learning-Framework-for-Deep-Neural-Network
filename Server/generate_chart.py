def generate_chart(mongodb_host):
    from Server.ModelAccuraciesRepository import ModelAccuraciesRepository

 

    db = ModelAccuraciesRepository(mongodb_host)

    strTable = "<html><table><tr><th>TimeStamp of Iteration</th><th>Number of users involved</th><th>Metric after iteration</th></tr>"

    info = db.get_clients_accuracies()[-10:]
    for i in info:
        strTable += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i[0], i[1], i[2])
    
    strTable = strTable+"</table></html>"
    
    return strTable