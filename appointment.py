from db import appointments


def check_slot(date, time):

    exists = appointments.find_one({
        "date": date,
        "time": time
    })

    return exists


def create_appointment(name, phone, service, date, time):

    if check_slot(date, time):

        return {
            "status": "unavailable",
            "message": "Slot already booked"
        }

    appointments.insert_one({
        "name": name,
        "phone": phone,
        "service": service,
        "date": date,
        "time": time
    })

    return {
        "status": "confirmed",
        "message": "Appointment booked successfully"
    }


def cancel_appointment(phone):

    appt = appointments.find_one({"phone": phone})

    if not appt:
        return {"status": "not_found"}

    appointments.delete_one({"phone": phone})

    return {"status": "cancelled"}