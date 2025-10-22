"""
Database Manager - Handles all database operations
"""
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="fleet_manager.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()
        
        # Vehicles table - UPDATED με όλα τα νέα fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_plate TEXT UNIQUE NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                vehicle_type TEXT,
                vin_number TEXT,
                mileage INTEGER DEFAULT 0,
                engine_cc INTEGER,
                fuel_type TEXT,
                color TEXT,
                notes TEXT,
                insurance_expiry TEXT,
                kteo_next TEXT,
                kek_renewal TEXT,
                status TEXT DEFAULT 'Active',
                has_gps INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if has_gps column exists, if not add it
        cursor.execute("PRAGMA table_info(vehicles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'has_gps' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN has_gps INTEGER DEFAULT 0")
        
        if 'vehicle_type' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN vehicle_type TEXT")
        
        if 'vin_number' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN vin_number TEXT")
        
        if 'engine_cc' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN engine_cc INTEGER")
        
        if 'notes' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN notes TEXT")
        
        if 'insurance_expiry' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN insurance_expiry TEXT")
        
        if 'kteo_next' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN kteo_next TEXT")
        
        if 'kek_renewal' not in columns:
            cursor.execute("ALTER TABLE vehicles ADD COLUMN kek_renewal TEXT")
        
        self.conn.commit()
    
    def add_vehicle(self, vehicle_data):
        """Add a new vehicle"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO vehicles (
                license_plate, brand, model, year, vehicle_type, vin_number,
                mileage, engine_cc, fuel_type, color, notes,
                insurance_expiry, kteo_next, kek_renewal, status, has_gps
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vehicle_data.get('license_plate'),
            vehicle_data.get('brand'),
            vehicle_data.get('model'),
            vehicle_data.get('year'),
            vehicle_data.get('vehicle_type'),
            vehicle_data.get('vin_number'),
            vehicle_data.get('mileage', 0),
            vehicle_data.get('engine_cc'),
            vehicle_data.get('fuel_type'),
            vehicle_data.get('color'),
            vehicle_data.get('notes'),
            vehicle_data.get('insurance_expiry'),
            vehicle_data.get('kteo_next'),
            vehicle_data.get('kek_renewal'),
            vehicle_data.get('status', 'Active'),
            vehicle_data.get('has_gps', 0)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_vehicles(self):
        """Get all vehicles"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        vehicles = []
        for row in rows:
            vehicles.append(dict(row))
        
        return vehicles
    
    def get_vehicle_by_license(self, license_plate):
        """Get vehicle by license plate"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM vehicles WHERE license_plate = ?
        """, (license_plate,))
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_vehicle_by_id(self, vehicle_id):
        """Get vehicle by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def update_vehicle(self, vehicle_id, vehicle_data):
        """Update vehicle information"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE vehicles SET
                license_plate = ?,
                brand = ?,
                model = ?,
                year = ?,
                vehicle_type = ?,
                vin_number = ?,
                mileage = ?,
                engine_cc = ?,
                fuel_type = ?,
                color = ?,
                notes = ?,
                insurance_expiry = ?,
                kteo_next = ?,
                kek_renewal = ?,
                status = ?,
                has_gps = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            vehicle_data.get('license_plate'),
            vehicle_data.get('brand'),
            vehicle_data.get('model'),
            vehicle_data.get('year'),
            vehicle_data.get('vehicle_type'),
            vehicle_data.get('vin_number'),
            vehicle_data.get('mileage'),
            vehicle_data.get('engine_cc'),
            vehicle_data.get('fuel_type'),
            vehicle_data.get('color'),
            vehicle_data.get('notes'),
            vehicle_data.get('insurance_expiry'),
            vehicle_data.get('kteo_next'),
            vehicle_data.get('kek_renewal'),
            vehicle_data.get('status'),
            vehicle_data.get('has_gps', 0),
            vehicle_id
        ))
        self.conn.commit()
    
    def delete_vehicle(self, license_plate):
        """Delete vehicle from database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE license_plate = ?", (license_plate,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_vehicles_with_gps(self):
        """Get all vehicles that have GPS trackers"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM vehicles 
            WHERE has_gps = 1 
            ORDER BY brand, model
        """)
        rows = cursor.fetchall()
        
        vehicles = []
        for row in rows:
            vehicles.append(dict(row))
        
        return vehicles
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
