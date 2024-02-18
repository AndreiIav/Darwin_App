"""Data models"""
from . import db


class Magazines(db.Model):

    __tablename__ = "magazines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    magazine_link = db.Column(db.Text)

    def __repr__(self):
        return f"Magazines(id={self.id},name={self.name},magazine_link={self.magazine_link})"


class MagazineYear(db.Model):

    __tablename__ = "magazine_year"

    id = db.Column(db.Integer, primary_key=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey("magazines.id"))
    year = db.Column(db.Text)
    magazine_year_link = db.Column(db.Text)

    def __repr__(self):
        return f"MagazineYear(id={self.id},magazine_id={self.magazine_id},year={self.year},magazine_year_link={self.magazine_year_link})"
        

class MagazineNumber(db.Model):

    __tablename__ = "magazine_number"

    id = db.Column(db.Integer, primary_key=True)
    magazine_year_id = db.Column(db.Integer, db.ForeignKey("magazine_year.id"))
    magazine_number = db.Column(db.Text)
    magazine_number_link = db.Column(db.Text)

    def __repr__(self):
        return f"MagazineNumber(id={self.id},magazine_year_id={self.magazine_year_id},magazine_number={self.magazine_number},magazine_number_link={self.magazine_number_link})"


class MagazineNumberContent(db.Model):

    __tablename__ = "magazine_number_content"

    id = db.Column(db.Integer, primary_key=True)
    magazine_number_id = db.Column(db.Integer, db.ForeignKey("magazine_number.id"))
    magazine_content = db.Column(db.Text)
    magazine_page = db.Column(db.Text)

    def __repr__(self):
        return f"MagazineNumberContent(id={self.id},magazine_number_id={self.magazine_number_id},magazine_content={self.magazine_content},magazine_page={self.magazine_page})"


class MagazineNumberContentFTS(db.Model):

    __tablename__ = "magazine_number_content_fts"

    rowid = db.Column(db.Integer, primary_key=True)
    magazine_content = db.Column(db.Text)

    def __repr__(self):
        return f"MagazineNumberContentFTS(rowid={self.rowid},magazine_content={self.magazine_content})"
    

class MagazineDetails(db.Model):

    __tablename__ = "magazine_details"

    id = db.Column(db.Integer, primary_key=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey("magazines.id"))
    year = db.Column(db.Text)
    distinct_magazine_numbers_count = db.Column(db.Integer)
    distinct_pages_count = db.Column(db.Integer)

    def __repr__(self):
        return f"MagazineDetails(id={self.id},magazine_id={self.magazine_id},year={self.year},distinct_magazine_numbers_count={self.distinct_magazine_numbers_count},distinct_pages_count={self.distinct_pages_count})"