class ListView:

    def __init__(self, objectList, propArray, actionArray):
        #objectList - array of objects with properties to serialise
        #propArray - array of dicts containing the property to serialise from objectList, and the name to display in the table header. Expect key of prop and name.
        #actionArray - array of action dicts to append to the end of each row. Expect keys of action and url. Action is the word to and url is the action. If the action requires a unique identifer, the key will be identifier.

        self.listheaders = [] #simple array of header names
        self.rows = [] #dictionary of data: dataArray, action: actionArray

        for propDict in propArray:
            self.listheaders.append(propDict['name']) #add each name to the header

        for obj in objectList:
            row = {}
            row['data'] = []
            row['actions'] = []
            for propDict in propArray:
                row['data'].append(str(getattr(obj, propDict['prop']))) #add array of data
            for action in actionArray:
                if 'identifier'in action:
                    url = action['url'] + "/" + str(getattr(obj, action['identifier']))
                else:
                    url = action['url']
                row['actions'].append({'action': action['action'], 'url': url})
            self.rows.append(row)

    def get_headers(self):
        return self.listheaders

    def get_rows(self):
        return self.rows

    def get_list(self):
        datadict = {'headers': self.listheaders, 'data': self.rows}
        return datadict
