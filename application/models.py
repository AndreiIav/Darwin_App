"""Data models"""
from . import db


class Magazines(db.Model):

    __tablename__ = "magazines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    magazine_link = db.Column(db.Text)

    to_magazine_year_relationship = db.relationship(
        "MagazineYear", back_populates="magazines_relationship"
    )

    def __repr__(self):
        return f"Magazine name: {self.name}, Magazine Link: {self.magazine_link}"


class MagazineYear(db.Model):

    __tablename__ = "magazine_year"

    id = db.Column(db.Integer, primary_key=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey("magazines.id"))
    year = db.Column(db.Text)
    magazine_year_link = db.Column(db.Text)

    magazines_relationship = db.relationship(
        "Magazines", back_populates="to_magazine_year_relationship"
    )
    magazine_number_relationship = db.relationship(
        "MagazineNumber", back_populates="from_magazine_year_relationship"
    )

    def __repr__(self):
        return (
            f"Magazine Year: {self.year}, Magazine_Year_Link: {self.magazine_year_link}"
        )


class MagazineNumber(db.Model):

    __tablename__ = "magazine_number"

    id = db.Column(db.Integer, primary_key=True)
    magazine_year_id = db.Column(db.Integer, db.ForeignKey("magazine_year.id"))
    magazine_number = db.Column(db.Text)
    magazine_number_link = db.Column(db.Text)

    from_magazine_year_relationship = db.relationship(
        "MagazineYear", back_populates="magazine_number_relationship"
    )
    magazine_number_content_relationship = db.relationship(
        "MagazineNumberContent", back_populates="magazine_number_relationship"
    )

    def __repr__(self):
        return f"Magazine Number: {self.magazine_number}, Magazine Number Link: {self.magazine_number_link}"


class MagazineNumberContent(db.Model):

    __tablename__ = "magazine_number_content"

    id = db.Column(db.Integer, primary_key=True)
    magazine_number_id = db.Column(db.Integer, db.ForeignKey("magazine_number.id"))
    magazine_content = db.Column(db.Text)
    magazine_page = db.Column(db.Text)

    magazine_number_relationship = db.relationship(
        "MagazineNumber", back_populates="magazine_number_content_relationship"
    )

    def __repr__(self):
        return f"Magazine Content: {self.magazine_content}, Magazine Page: {self.magazine_page}"
