export interface CustomUser {
    id: number;
    name: string;
    username: string;
    email: string;
    date_of_birth: string;
    hobbies: Hobby[];
    friends: Friendship[];
    profile_picture: string;
}

export interface MatchesUser {
    id: number,
    name: string,
    email: string,
    common_hobbies_count: number,
    hobbies: Hobby[],
    profile_picture: string | null,
    age: number
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

export interface Friendship {
    id: number;
    user_name: string;
    user_email: string;
    user_profile_picture: string;
    status: 'Pending' | 'Accepted';
    sent: boolean;
}