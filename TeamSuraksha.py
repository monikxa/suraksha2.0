import argparse
import face_recognition
import cv2

class FacialData:
    def __init__(self, id, name, location, timestamp, threat_level, image_path):
        self.id = id
        self.name = name
        self.location = location
        self.timestamp = timestamp
        self.threat_level = threat_level
        self.image_path = image_path

class FacialDatabase:
    def __init__(self):
        self.facial_data_list = []

    def add_facial_data(self, id, name, location, timestamp, threat_level, image_path):
        facial_data = FacialData(id, name, location, timestamp, threat_level, image_path)
        self.facial_data_list.append(facial_data)

class FaceRecognizer:
    def __init__(self, database):
        self.database = database

    def find_person_by_name(self, name):
        identified_persons = self.scan_faces(None, None, None)
        for person in identified_persons:
            if person.name == name:
                return person
        return None

    def scan_faces(self, location, timestamp, duration):
        video_path = "data/video.mp4"
        cap = cv2.VideoCapture(video_path)

        # Load the pre-trained face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#target_time = cv2.CAP_PROP_POS_MSEC
#cap.set(target_time, timestamp)

        identified_faces = set()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

          
            face_locations = face_recognition.face_locations(rgb_frame)

            for (top, right, bottom, left) in face_locations:
           
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                x = left
                y = top
                w = right - left
                h = bottom - top
                #ret = self.identify_face_of_region(rgb_frame, x, y, w, h, taylor_image_path)
                ret = self.find_match(rgb_frame, x, y, w, h)

                if (ret is not None):
                    print("---- SUCCESS ----")
                    identified_faces.add(ret)
                    cv2.putText(frame, ret.name, (left, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2, cv2.LINE_8)
                else:
                    print("No match in current frame")

       
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return identified_faces

    def find_match(self, frame, x, y, w, h):
        for p in self.database.facial_data_list:
            ret = self.identify_face_of_region(frame, x, y, w, h, p.image_path)
            print(" ", p.name, " ", p.image_path, " ", ret)
            if ret:
                return p
        return None
            
    def identify_face_of_region(self, frame, x, y, w, h, face_to_identify_image_path):
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image_to_match = cv2.imread(face_to_identify_image_path)
        gray_image_to_match = cv2.cvtColor(image_to_match, cv2.COLOR_BGR2GRAY)

        # Extract the region of interest (ROI) containing the face
        face_roi = gray_frame[y:y+h, x:x+w]

        # Resize the face ROI to match the size of the image to match
        face_roi_resized = cv2.resize(face_roi, (image_to_match.shape[1], image_to_match.shape[0]))

	    # Compare the face ROI with the image to match
        difference = cv2.absdiff(face_roi_resized, gray_image_to_match)
        mean_difference = difference.mean()
        print(mean_difference, end="")

        # Threshold for considering a match
        if mean_difference < 60:
            return True

        return False

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
    facial_database.add_facial_data(1, "Taylor Swift", "Location1", "2024-01-23 12:00:00", 1, 'data/taylor-swift.jpg')
    facial_database.add_facial_data(2, "Taylor Swift", "Location2", "2024-01-23 12:30:00", 2, 'data/taylor-swift.jpg')
    facial_database.add_facial_data(3, "Selena Gomez", "Location3", "2024-01-23 13:00:00", 3, 'data/selena-gomez.jpg')
    facial_database.add_facial_data(4, "Olivia Rodrigo", "Location1", "2024-01-23 14:00:00", 2, 'data/olivia-rodrigo.jpg')
    facial_database.add_facial_data(5, "Sabrina Carpenter", "Location4", "2024-01-23 14:30:00", 4, 'data/sabrina-carpenter.jpg')
    facial_database.add_facial_data(6, "Jennie Kim", "Location2", "2024-01-23 15:00:00", 1, 'data/jennie-kim.jpg')
    facial_database.add_facial_data(7, "Shawn Mendes", "Location3", "2024-01-23 15:30:00", 3, 'data/shawn-mendes.jpg')

    face_recognizer = FaceRecognizer(facial_database)

    if args.usage == "find_person":
        if not args.name:
            print("Error: Name argument is required for finding a person.")
            return

        result = face_recognizer.find_person_by_name(args.name)
        print("")
        print("---------------------------------------+")
        print("|                                      |")
        print("| Usage 1 Result:", result.name if result else "NOT FOUND")
        print("|                                      |")
        print("---------------------------------------+")

    elif args.usage == "scan_faces":
        if not args.location or not args.timestamp or not args.duration:
            print("Error: Location, timestamp, and duration arguments are required for face scanning.")
            return

        identified_faces = face_recognizer.scan_faces(args.location, args.timestamp, args.duration)
        print("")
        print("---------------------------------------+")
        print("|                                      |")
        print("| Usage 2 Result:")
        for face in identified_faces:
            print(f"| Name: {face.name}, Threat Level: {face.threat_level}")
        print("|                                      |")
        print("---------------------------------------+")
        threat_levels = face_recognizer.classify_threat_level(identified_faces)

        face_recognizer.alert_authorities(threat_levels, args.location)

if __name__ == "__main__":
    main()
