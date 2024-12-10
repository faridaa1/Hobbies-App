export interface CustomUser {
    id: number;
    name: string;
    email: string;
    password: string;
    date_of_birth: Date;
    hobbies: Hobby[];
    friends: Friendship[];
    profile_picture: string;
}

export interface Hobby {
    hobby_id: number;
    hobby_name: string;
    hobby_description: string
}

export interface UserHobby {
    user: CustomUser;
    hobby: Hobby;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    start_date: String;
}

export interface UserHobbies {
    user_hobbies: UserHobby[]
}

export interface Friendship {
    user_name: string;
    user_profile_picture: string;
    status: 'Pending' | 'Accepted';
    sent: boolean;
}