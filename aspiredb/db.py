import requests
from aspiredb.core.fileWriter import FileWriter
from aspiredb.core.encriptor import EncryptFile, EncryptMessage

class DBMS(
    FileWriter

    ):
    auth:list = ['shelango']
    url = 'http://vrstan:metador@localhost:5984/'
    resourse:dict = {
            'dump': f'{url}vrstan',
            'parted': f'{url}vrstan_pa',
            'employee': f'{url}employee',
            'project': f'{url}project',
            'task': f'{url}task',
            'reports': f'{url}reports',

        }
    
    def resolve_url(self, hand):       
        return self.resourse.get(hand, f'{self.url}{hand}')
    
    async def db_report(self, db):
        url = self.resolve_url(db)
        db_report = requests.get(url).json()
        return db_report

    async def db_changes(self, db="dump"):
        ''' Returns a list of recent changes on the database'''

        url = f"{self. resolve_url(db)}/_changes"
        report = requests.get(url).json()        
        return report.get('results') #list(found)    
    
    async def checkExist(self, db_name):
        check = await self.db_report(db_name)
        if "error" in check.keys():
            if check.get("error") == 'unauthorized':
                pass
            if check.get("error") == 'not_found':
                return False
            return False
        return True

    async def check_db(self, db_name):
        url = f"{self. resolve_url(db_name)}"
        check = requests.head(url)
        return {'status': check.status_code}

    async def createDb(self, db_name):
        if await self.checkExist(db_name):
            return {"error": "Database already exist."}        
        return requests.put(f"{self.resolve_url(db_name)}")
    
    # DATABASE COMPACTION
    async def compact(self, db_name):
        '''Starts a compaction for the database'''
        if await self.checkExist(db_name):
            return requests.post(f"{self.url}{db_name}/_compact", headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Host': 'localhost:5984'
            })
        return {"error": "Database does not exist"}
    
    # DESIGN DOCUMENTS
    @property
    async def setup_project_database(self):
        # 1 check for database

        # 2 create data base

        # 3 get design docuent from json file

        # save document to the new database
        pass

    async def create_design_doc(self, db_name, ddoc):
        '''Creates a new named design document, or creates a new revision of the existing design document.'''
        if await self.checkExist(db_name):
            return requests.put(f"{self.url}{db_name}/_design/{ddoc}").json()
        return {"error": "Database does not exist"}

    async def compact_design_doc(self, db_name, ddoc):
        '''Starts a compaction for all the views in 
        the selected design document'''
        if await self.checkExist(db_name):
            return requests.post(f"{self.url}{db_name}/_compact/{ddoc}", headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Host': 'localhost:5984'
            })
        return {"error": "Database does not exist"}

    async def get_design_doc(self, db_name, ddoc):
        '''Returns the contents of the design document
        specified with the name of the design document'''
        if await self.checkExist(db_name):
            return requests.get(f"{self.url}{db_name}/_design/{ddoc}").json()
        return {"error": "Database does not exist"}

    async def deleteDb(self, db_name, auth:dict=None):
        """ Accepts POST request only"""
        if await self.checkExist(db_name):            
            if self.is_auth(auth.get('code')):
                return requests.delete(f"{self. resolve_url(db_name)}").status_code
            return {
                "error": "Unautorized", 
                "status_message": 'You are not Authorised to perform that action.'}
        return {"error": "That Database does not exist."} 

    @property
    async def db_list(self):        
            return requests.get(f"{self.url}_all_dbs").json()

    def is_auth(self, auth):
        return  auth in self.auth

    async def replicate_local(self, source, destination):
        data = {
            "_id": "my_rep",
            "source": f"{self. resolve_url(source)}",
            "target": f"{self. resolve_url(destination)}",
            "create_target":  True,
            "continuous": True
        }
        return requests.post(f"{self.url}_replicate", json=data)
        #return {"statu": f'Started Replicating.  {source} < = > {destination}'}
               
    async def query_replication(self, rep_id):
        #return requests.get(f"{self.url}_scheduler/docs/_replicator/{rep_id}")
        pass

        

