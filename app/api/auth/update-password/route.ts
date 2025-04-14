import { NextRequest, NextResponse } from 'next/server';
import { updatePassword, getCurrentSession } from '@/lib/auth/local-auth';

export async function POST(request: NextRequest) {
  try {
    // Get authorization header
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const token = authHeader.replace('Bearer ', '');
    const session = getCurrentSession(token);
    
    if (!session) {
      return NextResponse.json(
        { error: 'Invalid or expired session' },
        { status: 401 }
      );
    }

    const { password } = await request.json();
    
    if (!password) {
      return NextResponse.json(
        { error: 'Password is required' },
        { status: 400 }
      );
    }
    
    const success = updatePassword(session.user.id, password);
    
    if (!success) {
      return NextResponse.json(
        { error: 'Failed to update password' },
        { status: 400 }
      );
    }
    
    return NextResponse.json({ user: session.user });
  } catch (error) {
    console.error('Update password error:', error);
    return NextResponse.json(
      { error: 'An error occurred while updating password' },
      { status: 500 }
    );
  }
} 