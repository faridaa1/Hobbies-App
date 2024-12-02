export interface CustomUser {
    id: number;
    name: string;
    email: string;
    date_of_birth: Date;
    hobbies: UserHobby[];
    friends: Friendship[];
    profile_picture: string | null
}

export interface Hobby {
    hobby_id: number;
    hobby_name: string;
    hobby_description: string
}

export interface UserHobby { 
    user: number;
    hobby: number;
    level: 'Beginner' | 'Intermediate' | 'Advanced';
    start_date: Date
}

export interface Friendship {
    user1: number;
    user2: number;
    status: 'Pending' | 'Accepted'
}