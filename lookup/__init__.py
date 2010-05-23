#!/usr/bin/env python
#
#    Greek New Testament
#    Copyright (C) 2010  Honza Pokorny <honza@honzapokorny.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import config

books = {
    '1 Corinthians': 'cor1',
    '1 John': 'john1',
    '1 Peter': 'peter1',
    '1 Thessalonians': 'thess1',
    '1 Timothy': 'tim1',
    '2 Corinthians': 'cor2',
    '2 John': 'john2',
    '2 Peter': 'peter2',
    '2 Thessalonians': 'thess2',
    '2 Timothy': 'tim2',
    '3 John': 'john3',
    'Acts': 'acts',
    'Colossians': 'col',
    'Ephesians': 'eph',
    'Galatians': 'gal',
    'Hebrews': 'heb',
    'James': 'james',
    'John': 'john',
    'Jude': 'jude',
    'Luke': 'luke',
    'Mark': 'mark',
    'Matthew': 'matthew',
    'Philemon': 'phm',
    'Phillipians': 'phil',
    'Revelation': 'revelation',
    'Romans': 'romans',
    'Titus': 'titus'
}

class LookUp:

    def __init__(self):
        self.connection = sqlite3.connect(config.db_name)
        self.cursor = self.connection.cursor()
        self.passage = ''
    
    def set_passage(self, passage):
        self.passage = self.extract_passage(passage)
        
    def extract_passage(self, passage):
        # 1 Cor 5:21 Luke 12:11
        result = []
        pieces = passage.split(" ")
        numbers = ''
        
        if len(pieces) == 2:
            result.append(pieces[0])
            numbers = pieces[1]
        elif len(pieces) == 3:
            numbers = pieces[2]
            name = []
            name.append(pieces[0])
            name.append(pieces[1])
            space = ' '
            long_book = space.join(name)
            result.append(long_book)
        
        n_pieces = numbers.split(":")
        result.append(n_pieces[0])
        result.append(n_pieces[1])
        
        return result
        
    def get_passage(self):
        return self.passage
            
    def get_db_name_for_book(self, book):
        if book in books:
            return books[book]
        else:
            return book
    
    
    def get_verse(self):
        book = str(self.get_db_name_for_book(self.passage[0]))
        chapter = self.passage[1]
        verse = self.passage[2]
        t = (chapter, verse,)
        m = self.cursor.execute('select * from ' + book + ' where chapter=? and verse=?', t)
        space = ' '
        words = []
        for a in m:
            words.append(a[2])

        result = space.join(words)
        return result
        
    def get_words(self):
        print 'get words...'
        book = str(self.get_db_name_for_book(self.passage[0]))
        chapter = self.passage[1]
        verse = self.passage[2]
        t = (chapter, verse,)
        print t
        m = self.cursor.execute('select * from ' + book + ' where chapter=? and verse=?', t)
        
        words = []
        for a in m:
            words.append(a)
        return words
        
    def get_hint(self):
        words = self.get_words()
        space = ' '
        new_words = []
        for word in words:
            definition = self.get_definition(word[4])
            st = str(word[2]) + ': ' + str(definition) + '\n----------------\n'
            new_words.append(st)
        
        result = space.join(new_words)
        return result
        
    def get_definition(self, number):
        t = (number,)
        m = self.cursor.execute('select * from strong where number=?', t)
        for a in m:
            return a[1]
    
    
        
