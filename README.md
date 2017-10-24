**** select directory to create virtual environment ****
virtualenv credr

source venv/bin/activate -- To activate virtual environment

*** clone the Git Repository ******

git clone https://github.com/kpurna/credr.git

install the requirements.txt file for installing required packages

Changes the database setting of your own in the credrApp/settings.py file

*** select the database and run the command to create required tables ******

CREATE TABLE invoice (
  invoice_id int(11) NOT NULL AUTO_INCREMENT,
  customer varchar(50) NOT NULL,
  date datetime NOT NULL,
  total_quantity varchar(20) NOT NULL,
  total_amount decimal(10,2) NOT NULL,
  PRIMARY KEY (invoice_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1


CREATE TABLE invoice_transactions (
  id int(11) NOT NULL AUTO_INCREMENT,
  invoice_id int(11) NOT NULL,
  product varchar(50) NOT NULL DEFAULT '',
  quantity int(11) NOT NULL DEFAULT '0',
  price decimal(10,2) NOT NULL DEFAULT '0.00',
  line_total decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (id),
  KEY invoice_id (invoice_id),
  CONSTRAINT invoice_transactions_ibfk_1 FOREIGN KEY (invoice_id) REFERENCES invoice (invoice_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1


python manage.py runserver -- To run project in local.


********Create a new record in db*****
method:POST
url: http://localhost:8000/v0/invoice-details/

{
"customer": "credr",
"transactions": [
    {
      "product": "pulsar",
      "quantity": 1,
      "price": 30
    }
  ]
}


********Update or edit record in db*****
method: PUT
url: http://localhost:8000/v0/invoice-details/

{
"id": 10,
"transactions": [
    {
      "product": "pulsar",
      "quantity": 1,
      "price": 30
    }
  ]
}


************ GET Record **************

http://localhost:8000/v0/invoice-details/    ///////// get all the records
http://localhost:8000/v2/invoice-details/9/ /// get particluar reordc with id specified



********Delete a new record in db*****
method:Delete
Url: http://localhost:8000/v0/invoice-details/

{
"id": 10
}