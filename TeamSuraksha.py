import argparse
import face_recognition
import cv2

class FacialData:
    def __init__(self, id, name, location, timestamp, threat_level):
        self.id = id
        self.name = name
        self.location = location
        self.timestamp = timestamp
        self.threat_level = threat_level

class FacialDatabase:
    def __init__(self):
        self.facial_data_list = []

    def add_facial_data(self, id, name, location, timestamp, threat_level):
        facial_data = FacialData(id, name, location, timestamp, threat_level)
        self.facial_data_list.append(facial_data)

    def find_person_by_name(self, name):
        for person in self.facial_data_list:
            if person.name == name:
                return person
        return None

class FaceRecognizer:
    def __init__(self, database):
        self.database = database

    def scan_faces(self, location, timestamp, duration):
        video_path= "vid.mp4"
        cap = cv2.VideoCapture(video_path)

        target_time = cv2.CAP_PROP_POS_MSEC
        cap.set(target_time, timestamp)

        identified_faces = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

          
            face_locations = face_recognition.face_locations(rgb_frame)

            for (top, right, bottom, left) in face_locations:
           
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

  
                identified_faces.append(FacialData(id=None, name=None, location=location, timestamp=timestamp, threat_level=None))

       
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return identified_faces

    def classify_threat_level(self, identified_faces):
        threat_levels = {}
        for face in identified_faces:
            threat_levels[face.name] = face.threat_level  # You can modify this based on your criteria
        return threat_levels

    def alert_authorities(self, threat_levels, location):
        num_people = len(threat_levels)
        
        if num_people >= 1:
            print(f"Alert: Level 4 - {num_people} person(s) identified in {location}")
        if num_people >= 4:
            print(f"Alert: Level 3 - {num_people} people identified simultaneously in {location}")

def main():
    parser = argparse.ArgumentParser(description="Facial Recognition System")
    parser.add_argument("usage", choices=["find_person", "scan_faces"], help="Select the usage type")
    parser.add_argument("--name", help="Name of the person (Usage 1)")
    parser.add_argument("--location", help="Location for face scanning (Usage 2)")
    parser.add_argument("--timestamp", type=int, help="Timestamp for face scanning (Usage 2)")
    parser.add_argument("--duration", type=int, help="Duration for face scanning (Usage 2)")
    
    args = parser.parse_args()

    facial_database = FacialDatabase()
    facial_database.add_facial_data(1, "Taylor Swift", "Location1", "2024-01-23 12:00:00", 1)
    facial_database.add_facial_data(2, "Taylor Swift", "Location2", "2024-01-23 12:30:00", 2)
    facial_database.add_facial_data(3, "Selena Gomez", "Location3", "2024-01-23 13:00:00", 3)
    facial_database.add_facial_data(4, "Olivia Rodrigo", "Location1", "2024-01-23 14:00:00", 2)
    facial_database.add_facial_data(5, "Sabrina Carpenter", "Location4", "2024-01-23 14:30:00", 4)
    facial_database.add_facial_data(6, "Jennie Kim", "Location2", "2024-01-23 15:00:00", 1)
    facial_database.add_facial_data(7, "Shawn Mendes", "Location3", "2024-01-23 15:30:00", 3)

    face_recognizer = FaceRecognizer(facial_database)

    if args.usage == "find_person":
        if not args.name:
            print("Error: Name argument is required for finding a person.")
            return

        result = facial_database.find_person_by_name(args.name)
        print("Usage 1 Result:", result.name if result else None)

    elif args.usage == "scan_faces":
        if not args.location or not args.timestamp or not args.duration:
            print("Error: Location, timestamp, and duration arguments are required for face scanning.")
            return

        identified_faces = face_recognizer.scan_faces(args.location, args.timestamp, args.duration)
        print("Usage 2 Result:")
        for face in identified_faces:
            print(f"Name: {face.name}, Threat Level: {face.threat_level}")

        threat_levels = face_recognizer.classify_threat_level(identified_faces)

        face_recognizer.alert_authorities(threat_levels, args.location)

if __name__ == "__main__":
    main()
