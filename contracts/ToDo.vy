# @version 0.3.3

# ToDo list per user
# Write/Read per sender
# Check if ToDo is complete

# 1. DECLARING INTERFACES

struct Task: 
    status: uint8
    description: String[128]
    owner: address
    taskId: uint256

# 2. DECLARING EVENTS

# 3. DECLARING STORAGE VARIABLES

OPEN: constant(uint8) = 0
IN_PROGRESS: constant(uint8) = 1
COMPLETE: constant(uint8) = 2
STATUSES: constant(uint8[3]) = [OPEN, IN_PROGRESS, COMPLETE]

totalTasks: public(uint256)
idToTask: public(HashMap[uint256, Task])
totalUserTasks: public(HashMap[address, uint256])
userTaskAt: public(HashMap[address, HashMap[uint256, uint256]])

# 4. DECLARING CALLS AND FUNCTIONS

@external
@nonpayable
def createTask(_status: uint8, _description: String[128]):
    assert _status in STATUSES, "INVALID STATUS"
    assert len(_description) > 0, "DESCRIPTION CAN NOT BE EMPTY"

    self.totalTasks += 1
    taskId: uint256 = self.totalTasks

    task: Task = Task({
        status: _status,
        description: _description,
        owner: msg.sender,
        taskId: taskId
    })

    self.idToTask[taskId] = task

    taskCount: uint256 = self.totalUserTasks[msg.sender]
    self.userTaskAt[msg.sender][taskCount] = taskId

    self.totalUserTasks[msg.sender] += 1
