import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;

import java.io.IOException;
import java.sql.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;

import java.util.*;
import java.util.concurrent.TimeUnit;

public class DerbyDBImport {
    private static final String usageMsg = "USAGE: java DerbyDBImport <DATASET FILEPATH> <DATABASE NAME> ";
    private static final String DATAFILE_DELIM = "\t";
    private static final int NUM_FIELDS_IN_DATASET = 9;

    private static final String businessNamesTableName = "BUSINESS_NAMES";
    private static final String statesTableName = "STATES";
    private static final String registeredTableName = "REGISTERED";
    private static final String businessRenewalsTableName = "RENEWALS";

    private static final Map<String, Integer> statesMap = new HashMap<String, Integer>() {{
        put("VIC", 1);
        put("NSW", 2);
        put("ACT", 3);
        put("QLD", 4);
        put("NT", 5);
        put("SA", 6);
        put("WA", 7);
        put("TAS", 8);
        put("NULL", 9);
    }};
    private static final Map<String, Integer> statusesMap = new HashMap<String, Integer>() {{
        put("Deregistered", 1);
        put("Registered", 2);
        put("NULL", 3);
    }};


    private static final Map<String, String> tables = new LinkedHashMap<String, String>() {{
        put(
                statesTableName,
                "(STATE_CODE INT, STATE_NAME VARCHAR(4), PRIMARY KEY(STATE_CODE))"
        );
        put(
                registeredTableName,
                "(REG_CODE INT, REG_TEXT VARCHAR(15), PRIMARY KEY(REG_CODE))"
        );
        put(
                businessNamesTableName,
                "(ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1), " +
                        "BN_NAME VARCHAR(256), REG_CODE INT REFERENCES registered(REG_CODE), " +
                        "BN_REG_DT DATE, BN_CANCEL_DT DATE, " +
                        "BN_STATE_NUM VARCHAR(15), STATE_CODE INT REFERENCES states(STATE_CODE), BN_ABN VARCHAR(15), " +
                        "PRIMARY KEY(ID))"
        );
        put(
                businessRenewalsTableName,
                "(ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1), " +
                        "RENEW_DATE DATE, BUSINESS_ID INT REFERENCES BUSINESS_NAMES(ID), " +
                        "PRIMARY KEY(ID))"
        );
    }};

    public static Connection dbConnect(String databaseName) throws SQLException {
        Properties connectionProps = new Properties();
//        connectionProps.put("user", "jb");
//        connectionProps.put("password", "password");

        String connectionURL = String.format("jdbc:derby:%s.db;create=true", databaseName);

        Connection conn = DriverManager.getConnection(
                connectionURL,
                connectionProps
        );

        System.err.format("Connected to: %s\n", databaseName);

        return conn;
    }

    public static void dropTables(Connection conn, Set<String> tableNames) throws SQLException {
        String dropTableStatement;
        Statement statement = conn.createStatement();
        int tableNameIndex = 3;

        // drop first because it has foreign key constraint on another table that gets dropped before it
        try {
            statement.executeUpdate(String.format("DROP TABLE %s", businessRenewalsTableName));
        } catch(SQLException e) {
            // table doesn't exist
        }

        DatabaseMetaData metadata = conn.getMetaData();
        ResultSet existingTableNames = metadata.getTables(null, null, "%", null);
        List existingTableNamesList = new LinkedList();

        while (existingTableNames.next()) {
            existingTableNamesList.add(existingTableNames.getString(tableNameIndex));
        }

        for (String table : tableNames) {
            if (!existingTableNamesList.contains(table)) {
                continue;
            }
            dropTableStatement = String.format("DROP TABLE %s", table);
            statement.executeUpdate(dropTableStatement);
            System.err.format("Dropped table: %s\n", table);
        }
    }

    public static void createTables(Connection conn, Map<String, String> tablesWithDescriptions) throws SQLException {
        Statement statement = conn.createStatement();

        for (String tableName : tablesWithDescriptions.keySet()) {
            String tableDefinition = tablesWithDescriptions.get(tableName);
            String createTableStatement = String.format("CREATE TABLE %s%s", tableName, tableDefinition);
            statement.executeUpdate(createTableStatement);
            System.err.format("Created table: %s\n", tableName);
        }
    }

    public static void importData(Connection conn, String dataFilepath) throws FileNotFoundException, IOException{
        int insertedRecords = 0;

        // Enter the 'ENUM' type values for the Australian States
        try {
            Statement statement = conn.createStatement();
            for (String state : statesMap.keySet()) {
                String insertStmt = String.format("INSERT INTO %s (STATE_CODE, STATE_NAME) VALUES (%d, '%s')", statesTableName, statesMap.get(state), state);
                statement.executeUpdate(insertStmt);
            }
        } catch(SQLException e) {
            System.err.println(e.getMessage());
        }

        // Enter the allowed Status values
        try {
            Statement statement = conn.createStatement();
            for (String status : statusesMap.keySet()) {
                String insertStmt = String.format("INSERT INTO %s (REG_CODE, REG_TEXT) VALUES (%d, '%s')", registeredTableName, statusesMap.get(status), status);
                statement.executeUpdate(insertStmt);
            }
        } catch(SQLException e) {
            System.err.println(e.getMessage());
        }


        String line;
        BufferedReader reader = new BufferedReader(new FileReader(dataFilepath));
        reader.readLine(); // 'eat' the header line

        while((line = reader.readLine()) != null) {
            try {
                insertRecord(conn, line, insertedRecords+1);
                insertedRecords++;
            } catch(SQLException e) {
                System.err.println(e.getMessage());
            }

            if (insertedRecords % 100000 == 0) {
                System.err.format("Inserted %d records\n", insertedRecords);
            }
        }

        reader.close();
    }

    private static void insertRecord(Connection conn, String line, int currentBusinessId) throws SQLException {
        SimpleDateFormat parser = new SimpleDateFormat("dd/MM/yyyy");
        java.util.Date date;
        java.util.Date renewDate = null;
        String insertStatement = String.format(
                "INSERT INTO %s (BN_NAME, REG_CODE, BN_REG_DT, BN_CANCEL_DT, BN_STATE_NUM, STATE_CODE, BN_ABN) VALUES (?,?,?,?,?,?,?)",
                businessNamesTableName
        );
        String[] items = line.split(DATAFILE_DELIM);

        if (items.length != NUM_FIELDS_IN_DATASET) {
            items = Arrays.copyOf(items, NUM_FIELDS_IN_DATASET); // pad with nulls
        }

        PreparedStatement preparedStatement = conn.prepareStatement(insertStatement);
        int firstDate = 3;
        int lastDate = 4;
        for (int i = firstDate; i < lastDate+1; i++) {
            try {
                date = parser.parse(items[i]);
                java.sql.Date sqlDate = new java.sql.Date(date.getTime());
                preparedStatement.setDate(i, sqlDate);
            } catch(ParseException e) {
                preparedStatement.setDate(i, null);
            }
        }

        // get the renewal date for insertion into separate table
        try {
            renewDate = parser.parse(items[5]);
        } catch(ParseException e) {
            renewDate = null;
        }

        // Ignore the first column (0)
        preparedStatement.setString(1, items[1]);
        if (items[2] != null && !items[2].equals("")) {
            int status = statusesMap.get(items[2]);
            preparedStatement.setInt(2, status);
        } else {
            preparedStatement.setInt(2, statusesMap.get("NULL"));
        }
        preparedStatement.setString(5, items[6]);
        if (items[7] != null && !items[7].equals("")) {
            int state = statesMap.get(items[7]);
            preparedStatement.setInt(6, state);
        } else {
            preparedStatement.setInt(6, statesMap.get("NULL"));
        }
        preparedStatement.setString( 7, items[8]);

        preparedStatement.executeUpdate();
        insertRenewalDateRecord(conn, renewDate, currentBusinessId);
    }

    private static void insertRenewalDateRecord(Connection conn, java.util.Date renewDate, int businessId) throws SQLException {
        if (renewDate == null) {
            return;
        }

        String insertStatement = String.format(
                "INSERT INTO %s (RENEW_DATE, BUSINESS_ID) VALUES (?,?)",
                businessRenewalsTableName
        );
        PreparedStatement preparedStatement = conn.prepareStatement(insertStatement);

        java.sql.Date sqlDate = new java.sql.Date(renewDate.getTime());
        preparedStatement.setDate(1, sqlDate);
        preparedStatement.setInt(2, businessId);
        preparedStatement.executeUpdate();
    }

    private static String parseDatasetFilepath(String[] args) {
        if (args.length < 1) {
            return null;
        }
        return args[0];
    }

    private static String parseDatabaseName(String[] args) {
        if (args.length < 2) {
            return null;
        }
        return args[1];
    }

    public static void main(String[] args) {
        Connection connection;
        long executionTimeInMilliseconds = 0;

        String datasetFilepath = parseDatasetFilepath(args);
        String databaseName = parseDatabaseName(args);
        if (datasetFilepath == null || databaseName == null) {
            System.err.println(usageMsg);
            System.exit(1);
        }

        try {
            connection = dbConnect(databaseName);

            Set<String> tableNames = tables.keySet();
            dropTables(connection, tableNames);
            createTables(connection, tables);

            final long startTime = System.nanoTime();

            importData(connection, datasetFilepath);

            final long duration = System.nanoTime() - startTime;
            executionTimeInMilliseconds = TimeUnit.NANOSECONDS.toMillis(duration);
        } catch(SQLException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        } catch(FileNotFoundException e) {
            System.err.format("Datafile could not be found: %s\n", e.getMessage());
            System.exit(1);
        } catch(IOException e) {
            System.err.format("Error while reading datafile: %s\n", e.getMessage());
        }

        System.out.format("Total execution time (ms): %d\n", executionTimeInMilliseconds);
    }
}
